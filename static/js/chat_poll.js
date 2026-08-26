(function() {
    const config = window.kinBechChat || {};
    const conversationId = config.conversationId;
    const myUserId = config.myUserId;
    let lastMessageId = config.lastMessageId || 0;

    if (!conversationId || !myUserId) {
        return;
    }

    async function pollMessages() {
        const res = await fetch(`/messaging/api/conversation/${conversationId}/new-messages/?last_id=${lastMessageId}`);
        if (!res.ok) return;

        const data = await res.json();
        if (data.messages && data.messages.length) {
            const container = document.getElementById("messages-container");
            data.messages.forEach(function (m) {
                const isMe = m.sender_id === myUserId;
                const bubble = document.createElement("div");
                bubble.className = "message-bubble " + (isMe ? "me" : "other");
                bubble.textContent = m.text;
                container.appendChild(bubble);
                lastMessageId = Math.max(lastMessageId, m.id);
            });
            container.scrollTop = container.scrollHeight;
        }
    }

    setInterval(pollMessages, 2500);
})();