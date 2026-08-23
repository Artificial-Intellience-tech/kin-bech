from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Conversation, Message, ConversationMember
from accounts.models import User

@login_required
def conversations_list(request):
    conversations = Conversation.objects.filter(
        conversationmember__user=request.user
    ).distinct().order_by('-updated_at')
    return render(request, 'messaging/conversations.html', {'conversations': conversations})

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if not ConversationMember.objects.filter(conversation=conversation, user=request.user).exists():
        return redirect('conversations')
    
    messages = conversation.messages.all()
    other_user = conversation.participants.exclude(id=request.user.id).first()

    if request.method == 'POST':
        text = request.POST.get('text')
        if text.strip():
            Message.objects.create(conversation=conversation, sender=request.user, text=text)
            return redirect('conversation_detail', conversation_id=conversation.id)

    return render(request, 'messaging/conversation_detail.html', {
        'conversation': conversation,
        'messages': messages,
        'other_user': other_user
    })

@login_required
def start_conversation(request, username):
    other_user = get_object_or_404(User, username=username)
    if other_user == request.user:
        return redirect('profile', username=username)

    existing = Conversation.objects.filter(
        conversationmember__user=request.user
    ).filter(
        conversationmember__user=other_user
    ).distinct().first()

    if not existing:
        conversation = Conversation.objects.create()
        ConversationMember.objects.create(conversation=conversation, user=request.user)
        ConversationMember.objects.create(conversation=conversation, user=other_user)
    else:
        conversation = existing

    return redirect('conversation_detail', conversation_id=conversation.id)