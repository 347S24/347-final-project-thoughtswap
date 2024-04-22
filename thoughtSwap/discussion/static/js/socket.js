console.log("socket.js loaded");
let chatSocket;

function connect(code) {
    return new Promise((resolve, reject) => {
        console.log('Connecting to chat...', code);
        chatSocket = new WebSocket(
            'ws://' + window.location.host + 
            '/ws/discussion/' + code + '/'
        );

        console.log('chatsocket', chatSocket)

        chatSocket.onopen = function(e) {
            resolve();
        };

        chatSocket.onerror = function(e) {
            reject(new Error("Failed to connect"));
        };
        chatSocket.onmessage = function (e) {
            const data = JSON.parse(e.data);
            let div = document.createElement('div');
            div.className = 'response-item';
            div.innerHTML = data.message + '\n';
            document.querySelector('#response-board').appendChild(div);
        };
    });
}

function disconnect() {
    if (chatSocket) {
        chatSocket.close();
    }
}

function sendMessage(message) {
    if (chatSocket) {
        chatSocket.send(JSON.stringify({
            'message': message
        }));
    }
}

// export { connect, disconnect, sendMessage };