document.getElementById('chatbot-send').onclick = async function() {
    const input = document.getElementById('chatbot-input');
    const msg = input.value.trim();
    if (!msg) return;
    addMessage('You', msg);
    input.value = '';
    let location = '';
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(pos => {
            location = `${pos.coords.latitude},${pos.coords.longitude}`;
            sendToBot(msg, location);
        }, () => {
            sendToBot(msg, '');
        });
    } else {
        sendToBot(msg, '');
    }
};

function addMessage(sender, text) {
    const messages = document.getElementById('chatbot-messages');
    const div = document.createElement('div');
    div.innerHTML = `<strong>${sender}:</strong> ${text}`;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
}

async function sendToBot(msg, location) {
    addMessage('Bot', 'Thinking...');
    const res = await fetch('http://127.0.0.1:5000/api/ask', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ message: msg, location: location })
    });
    const data = await res.json();
    document.getElementById('chatbot-messages').lastChild.remove(); 
    if (data.reply) {
        addMessage('Bot', data.reply);
    } else {
        addMessage('Bot', 'Sorry, I could not process your request.');
    }

}
