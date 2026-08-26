from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.conversations_list, name='conversations'),
    path('messages/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('messages/start/<str:username>/', views.start_conversation, name='start_conversation'),

    # API for polling new messages
    path('api/conversation/<int:conversation_id>/new-messages/', views.get_new_messages, name='api_new_messages'),
]