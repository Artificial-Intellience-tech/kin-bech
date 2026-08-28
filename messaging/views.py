from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Conversation, Message, ConversationMember
from accounts.models import User


@login_required
def conversations_list(request):
    conversations = Conversation.objects.filter(
        conversationmember__user=request.user
    ).distinct().order_by('-updated_at')

    conv_data = []

    for conv in conversations:
        other_user = conv.participants.exclude(id=request.user.id).first()
        last_message = conv.messages.order_by('-created_at').first()

        conv_data.append({
            "conversation": conv,
            "other_user": other_user,
            "last_message": last_message,
        })

    return render(
        request,
        "messaging/conversations.html",
        {"conv_data": conv_data}
    )

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if not ConversationMember.objects.filter(conversation=conversation, user=request.user).exists():
        return redirect('conversations')
    
    messages = conversation.messages.all()
    other_user = conversation.participants.exclude(id=request.user.id).first()

    # Mark messages from the other user as read
    if other_user:
        Message.objects.filter(
            conversation=conversation,
            sender=other_user,
            is_read=False
        ).update(is_read=True)

    if request.method == 'POST':
        text = request.POST.get('text')
        if text and text.strip():
            Message.objects.create(conversation=conversation, sender=request.user, text=text)
            return redirect('conversation_detail', conversation_id=conversation.id)

    last_message_id = messages.last().id if messages.exists() else 0

    return render(request, 'messaging/conversation_detail.html', {
        'conversation': conversation,
        'messages': messages,
        'other_user': other_user,
        'last_message_id': last_message_id,
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


@login_required
def get_new_messages(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if not ConversationMember.objects.filter(conversation=conversation, user=request.user).exists():
        return JsonResponse({"messages": []}, status=403)

    last_id = int(request.GET.get("last_id", 0))
    messages = (
        Message.objects
        .filter(conversation=conversation, id__gt=last_id)
        .order_by("created_at")
    )
    data = [
        {
            "id": m.id,
            "sender_id": m.sender.id,
            "sender_username": m.sender.username,
            "text": m.text,
            "created_at": m.created_at.isoformat(),
        }
        for m in messages
    ]
    return JsonResponse({"messages": data})