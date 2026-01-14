from django.urls import path

from . import views


urlpatterns = [
    path('items/', views.list_items, name='auction-list-items'),
    path('items/create/', views.create_item, name='auction-create-item'),
    path('items/<int:item_id>/', views.item_detail, name='auction-item-detail'),
    path('items/<int:item_id>/bids/', views.place_bid, name='auction-place-bid'),
    path('items/<int:item_id>/questions/', views.post_question, name='auction-post-question'),
    path('questions/<int:question_id>/answers/', views.post_answer, name='auction-post-answer'),
]
