$(document).ready(function () {
    $('#send-button').click(function () {
        let question = $('#question-input').val().trim();
        if (question !== "") {
            appendChatBubble(question, 'user');
            $('#question-input').val('');

            $.ajax({
                url: '/ask',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ question: question }),
                beforeSend: function() {
                    appendChatBubble('Fetching response Plz wait...', 'ai', true);
                },
                success: function (response) {
                    $('.loading').last().remove();
                    appendChatBubble(response.response, 'ai');
                }
            });
        }
    });
});

function appendChatBubble(text, sender, isLoading = false) {
    let bubbleClass = sender === 'user' ? 'user-bubble' : 'ai-bubble';
    let loadingClass = isLoading ? 'loading' : '';
    let bubble = `<div class="chat-bubble ${bubbleClass} ${loadingClass}">${text}</div>`;
    $('#chat-container').append(bubble);
    $('#chat-container').scrollTop($('#chat-container')[0].scrollHeight);
}
