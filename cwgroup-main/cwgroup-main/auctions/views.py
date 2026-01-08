from __future__ import annotations

import json
from decimal import Decimal
from typing import Any, Dict, Optional

from django.contrib.auth import get_user_model
from django.db import models
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt

from .models import Answer, Bid, Item, Question
from .services import is_auction_ended, select_winning_bid, validate_bid

User = get_user_model()


def _json_error(message: str, status: int = 400) -> JsonResponse:
    return JsonResponse({'error': message}, status=status)


def _parse_json_body(request: HttpRequest) -> Optional[Dict[str, Any]]:
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return None


def _parse_datetime(value: str) -> Optional[timezone.datetime]:
    parsed = parse_datetime(value)
    if parsed is None:
        return None
    if timezone.is_naive(parsed):
        return timezone.make_aware(parsed)
    return parsed


@csrf_exempt
def create_item(request: HttpRequest) -> JsonResponse:
    if request.method != 'POST':
        return _json_error('POST required.', status=405)

    payload = _parse_json_body(request)
    if payload is None:
        return _json_error('Invalid JSON payload.')

    owner_id = payload.get('owner_id')
    title = payload.get('title')
    description = payload.get('description', '')
    starting_price = payload.get('starting_price')
    end_time_raw = payload.get('end_time')

    if not owner_id or not title or starting_price is None or not end_time_raw:
        return _json_error('owner_id, title, starting_price, and end_time are required.')

    end_time = _parse_datetime(str(end_time_raw))
    if end_time is None:
        return _json_error('end_time must be an ISO-8601 datetime string.')

    owner = get_object_or_404(User, pk=owner_id)
    item = Item.objects.create(
        owner=owner,
        title=title,
        description=description,
        starting_price=Decimal(str(starting_price)),
        end_time=end_time,
    )

    return JsonResponse({'id': item.id, 'message': 'Item created.'}, status=201)


def list_items(request: HttpRequest) -> JsonResponse:
    if request.method != 'GET':
        return _json_error('GET required.', status=405)

    query = request.GET.get('q', '').strip()
    items = Item.objects.all()
    if query:
        items = items.filter(models.Q(title__icontains=query) | models.Q(description__icontains=query))

    data = [
        {
            'id': item.id,
            'title': item.title,
            'description': item.description,
            'starting_price': str(item.starting_price),
            'end_time': item.end_time.isoformat(),
            'has_ended': is_auction_ended(item),
        }
        for item in items
    ]
    return JsonResponse({'items': data})


def item_detail(request: HttpRequest, item_id: int) -> JsonResponse:
    if request.method != 'GET':
        return _json_error('GET required.', status=405)

    item = get_object_or_404(Item, pk=item_id)
    winning_bid = select_winning_bid(item)
    data = {
        'id': item.id,
        'title': item.title,
        'description': item.description,
        'starting_price': str(item.starting_price),
        'end_time': item.end_time.isoformat(),
        'has_ended': is_auction_ended(item),
        'winning_bid': None,
        'bids': [
            {
                'id': bid.id,
                'bidder_id': bid.bidder_id,
                'amount': str(bid.amount),
                'created_at': bid.created_at.isoformat(),
            }
            for bid in item.bids.order_by('-amount', 'created_at')
        ],
        'questions': [
            {
                'id': question.id,
                'asker_id': question.asker_id,
                'text': question.text,
                'created_at': question.created_at.isoformat(),
                'answer': {
                    'id': question.answer.id,
                    'responder_id': question.answer.responder_id,
                    'text': question.answer.text,
                    'created_at': question.answer.created_at.isoformat(),
                }
                if hasattr(question, 'answer')
                else None,
            }
            for question in item.questions.all()
        ],
    }

    if winning_bid:
        data['winning_bid'] = {
            'id': winning_bid.id,
            'bidder_id': winning_bid.bidder_id,
            'amount': str(winning_bid.amount),
        }

    return JsonResponse(data)


@csrf_exempt
def place_bid(request: HttpRequest, item_id: int) -> JsonResponse:
    if request.method != 'POST':
        return _json_error('POST required.', status=405)

    payload = _parse_json_body(request)
    if payload is None:
        return _json_error('Invalid JSON payload.')

    bidder_id = payload.get('bidder_id')
    amount_raw = payload.get('amount')
    if not bidder_id or amount_raw is None:
        return _json_error('bidder_id and amount are required.')

    item = get_object_or_404(Item, pk=item_id)
    bidder = get_object_or_404(User, pk=bidder_id)
    amount = Decimal(str(amount_raw))

    validation = validate_bid(item, amount)
    if not validation.is_valid:
        return JsonResponse(
            {
                'error': validation.reason,
                'minimum_required': str(validation.minimum_required),
            },
            status=400,
        )

    bid = Bid.objects.create(item=item, bidder=bidder, amount=amount)
    return JsonResponse({'id': bid.id, 'message': 'Bid placed.'}, status=201)


@csrf_exempt
def post_question(request: HttpRequest, item_id: int) -> JsonResponse:
    if request.method != 'POST':
        return _json_error('POST required.', status=405)

    payload = _parse_json_body(request)
    if payload is None:
        return _json_error('Invalid JSON payload.')

    asker_id = payload.get('asker_id')
    text = payload.get('text')
    if not asker_id or not text:
        return _json_error('asker_id and text are required.')

    item = get_object_or_404(Item, pk=item_id)
    asker = get_object_or_404(User, pk=asker_id)

    question = Question.objects.create(item=item, asker=asker, text=text)
    return JsonResponse({'id': question.id, 'message': 'Question posted.'}, status=201)


@csrf_exempt
def post_answer(request: HttpRequest, question_id: int) -> JsonResponse:
    if request.method != 'POST':
        return _json_error('POST required.', status=405)

    payload = _parse_json_body(request)
    if payload is None:
        return _json_error('Invalid JSON payload.')

    responder_id = payload.get('responder_id')
    text = payload.get('text')
    if not responder_id or not text:
        return _json_error('responder_id and text are required.')

    question = get_object_or_404(Question, pk=question_id)
    if hasattr(question, 'answer'):
        return _json_error('Question already has an answer.')

    responder = get_object_or_404(User, pk=responder_id)
    answer = Answer.objects.create(question=question, responder=responder, text=text)
    return JsonResponse({'id': answer.id, 'message': 'Answer posted.'}, status=201)
