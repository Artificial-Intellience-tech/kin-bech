(function () {
    const container = document.getElementById("messages-container");

    if (!container) {
        return;
    }

    const conversationId = Number(container.dataset.conversationId);
    const myUserId = Number(container.dataset.userId);
    let lastMessageId = Number(container.dataset.lastMessageId);

    if (!conversationId || !myUserId || Number.isNaN(lastMessageId)) {
        return;
    }

    function addMessage(message) {
        const isMine = Number(message.sender_id) === myUserId;
        const bubble = document.createElement("div");

        bubble.className = isMine
            ? "message-bubble me"
            : "message-bubble other";

        bubble.textContent = message.text;
        container.appendChild(bubble);
    }

    async function pollMessages() {
        try {
            const response = await fetch(
                `/api/conversation/${conversationId}/new-messages/?last_id=${lastMessageId}`,
                {
                    headers: {
                        "X-Requested-With": "XMLHttpRequest"
                    }
                }
            );

            if (!response.ok) {
                return;
            }

            const data = await response.json();

            if (!data.messages || data.messages.length === 0) {
                return;
            }

            data.messages.forEach(function (message) {
                addMessage(message);
                lastMessageId = Math.max(lastMessageId, Number(message.id));
            });

            container.scrollTop = container.scrollHeight;
        } catch (error) {
            console.error("Could not fetch new messages:", error);
        }
    }

    container.scrollTop = container.scrollHeight;
    setInterval(pollMessages, 2500);
})();