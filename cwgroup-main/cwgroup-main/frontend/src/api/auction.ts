import { fetchJson } from './client';
import type { Bid, ItemDetail, ItemSummary, Question, WinningBid } from '../types';

export interface ItemListResponse {
    items: ItemSummary[];
}

export interface ItemDetailResponse {
    item: ItemDetail;
}

export interface CreateItemPayload {
    ownerId: number;
    title: string;
    description: string;
    startingPrice: number;
    endTime: string;
}

interface ApiItemSummary {
    id: number;
    title: string;
    description: string;
    starting_price: string;
    end_time: string;
    has_ended: boolean;
}

interface ApiBid {
    id: number;
    bidder_id: number;
    amount: string;
    created_at: string;
}

interface ApiAnswer {
    id: number;
    responder_id: number;
    text: string;
    created_at: string;
}

interface ApiQuestion {
    id: number;
    asker_id: number;
    text: string;
    created_at: string;
    answer: ApiAnswer | null;
}

interface ApiWinningBid {
    id: number;
    bidder_id: number;
    amount: string;
}

interface ApiItemDetail extends ApiItemSummary {
    bids: ApiBid[];
    questions: ApiQuestion[];
    winning_bid: ApiWinningBid | null;
}

interface ApiItemListResponse {
    items: ApiItemSummary[];
}

const mapItemSummary = (item: ApiItemSummary): ItemSummary => ({
    id: item.id,
    title: item.title,
    description: item.description,
    startingPrice: Number(item.starting_price),
    endTime: item.end_time,
    hasEnded: item.has_ended,
});

const mapBid = (bid: ApiBid): Bid => ({
    id: bid.id,
    bidderId: bid.bidder_id,
    amount: Number(bid.amount),
    createdAt: bid.created_at,
});

const mapAnswer = (answer: ApiAnswer): Question['answer'] => ({
    id: answer.id,
    responderId: answer.responder_id,
    text: answer.text,
    createdAt: answer.created_at,
});

const mapQuestion = (question: ApiQuestion): Question => ({
    id: question.id,
    askerId: question.asker_id,
    text: question.text,
    createdAt: question.created_at,
    answer: question.answer ? mapAnswer(question.answer) : null,
});

const mapWinningBid = (winningBid: ApiWinningBid | null): WinningBid | null =>
    winningBid
        ? {
              id: winningBid.id,
              bidderId: winningBid.bidder_id,
              amount: Number(winningBid.amount),
          }
        : null;

const mapItemDetail = (item: ApiItemDetail): ItemDetail => ({
    ...mapItemSummary(item),
    bids: item.bids.map(mapBid),
    questions: item.questions.map(mapQuestion),
    winningBid: mapWinningBid(item.winning_bid),
});

export const getItems = async (query?: string): Promise<ItemListResponse> => {
    const params = query ? `?q=${encodeURIComponent(query)}` : '';
    const response = await fetchJson<ApiItemListResponse>(`/auctions/items/${params}`);
    return {
        items: response.items.map(mapItemSummary),
    };
};

export const getItem = async (itemId: number): Promise<ItemDetailResponse> => {
    const response = await fetchJson<ApiItemDetail>(`/auctions/items/${itemId}/`);
    return {
        item: mapItemDetail(response),
    };
};

export const createItem = (payload: CreateItemPayload) =>
    fetchJson<{ id: number }>('/auctions/items/create/', {
        method: 'POST',
        body: JSON.stringify({
            owner_id: payload.ownerId,
            title: payload.title,
            description: payload.description,
            starting_price: payload.startingPrice,
            end_time: payload.endTime,
        }),
    });

export const placeBid = (itemId: number, payload: { bidderId: number; amount: number }) =>
    fetchJson<{ id: number }>(`/auctions/items/${itemId}/bids/`, {
        method: 'POST',
        body: JSON.stringify({
            bidder_id: payload.bidderId,
            amount: payload.amount,
        }),
    });

export const postQuestion = (itemId: number, payload: { askerId: number; text: string }) =>
    fetchJson<{ id: number }>(`/auctions/items/${itemId}/questions/`, {
        method: 'POST',
        body: JSON.stringify({
            asker_id: payload.askerId,
            text: payload.text,
        }),
    });

export const postAnswer = (questionId: number, payload: { responderId: number; text: string }) =>
    fetchJson<{ id: number }>(`/auctions/questions/${questionId}/answers/`, {
        method: 'POST',
        body: JSON.stringify({
            responder_id: payload.responderId,
            text: payload.text,
        }),
    });
