from django.contrib import admin

from .models import Answer, Bid, Item, Question


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'starting_price', 'end_time', 'winner_notified_at')
    search_fields = ('title', 'description', 'owner__username')
    list_filter = ('end_time',)


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'bidder', 'amount', 'created_at')
    list_filter = ('created_at',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'asker', 'created_at')
    search_fields = ('text',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'responder', 'created_at')
