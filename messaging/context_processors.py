from .models import Message, ConversationMember

def unread_msg_count(request):
    if not request.user.is_authenticated:
        return {"unread_msg_count": 0}

    # IDs of conversations this user is part of
    conversation_ids = list(
        ConversationMember.objects
        .filter(user=request.user)
        .values_list("conversation_id", flat=True)
    )

    if not conversation_ids:
        return {"unread_msg_count": 0}

    # Count unread messages in those conversations, excluding messages sent by the user
    count = Message.objects.filter(
        conversation_id__in=conversation_ids,
        is_read=False,
    ).exclude(sender=request.user).count()

    return {"unread_msg_count": count}