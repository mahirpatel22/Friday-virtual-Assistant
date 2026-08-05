const statusText = document.getElementById('statusText');
const userSpeech = document.getElementById('userSpeech');
const aiResponse = document.getElementById('aiResponse');

// Expose updateUI function to Python Eel backend
eel.expose(updateUI);

function updateUI(state, userText = "", assistantText = "") {
    // Reset state classes on body
    document.body.classList.remove('listening', 'speaking');

    if (state === 'listening') {
        document.body.classList.add('listening');
        statusText.innerText = 'Listening...';
        if (userText) userSpeech.innerText = userText;
        if (assistantText) aiResponse.innerText = assistantText;
    } 
    else if (state === 'speaking') {
        document.body.classList.add('speaking');
        statusText.innerText = 'Friday Active';
        if (userText) userSpeech.innerText = `"${userText}"`;
        if (assistantText) aiResponse.innerText = assistantText;
    } 
    else if (state === 'idle') {
        statusText.innerText = 'Say "Friday" to Wake';
        if (userText) userSpeech.innerText = userText;
        if (assistantText) aiResponse.innerText = assistantText;
    }
}