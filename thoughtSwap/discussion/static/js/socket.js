console.log("socket.js loaded");
// same socket across pages ?

function connectChat(code) {
    return new Promise((resolve, reject) => {
        console.log('Connecting to chat...', code);
        chatSocket = new WebSocket(
            'ws://' + window.location.host +
            '/ws/discussion/' + code + '/'
        );

        console.log('chatsocket', chatSocket)

        chatSocket.onopen = function (e) {
            resolve();
        };

        chatSocket.onerror = function (e) {
            reject(new Error("Failed to connect"));
        };
        chatSocket.onmessage = function (e) {
            const data = JSON.parse(e.data);
            console.log('data', data)
            if (data.message) {
                console.log('message', data.message)
                let div = document.createElement('div');
                div.className = 'response-item';
                div.innerHTML = data.message + '\n';
                
                // if no url, do not display delete button
                if (deleteGroupUrl) {
                    console.log('fac view delete element')
                    let img = document.createElement('img');
                    img.src = "/static//media/trash-svgrepo-com.svg";
                    img.alt = 'delete thought';
                    
                    let link = document.createElement('a');
                    link.className = 'ud-button delete-thought';
                    console.log(deleteGroupUrl)
                    link.href = deleteGroupUrl;
                    link.appendChild(img);
    
                    let tip_container = document.createElement('div');
                    tip_container.className = 'tip-container';
                    tip_container.appendChild(link);
                    div.appendChild(tip_container);
                }
                document.querySelector('#response-board').appendChild(div);
            }
            if (data.prompt) {
                console.log('prompt', prompt)
                let p = document.createElement('p');
                p.textContent = data.prompt + '\n';
                document.querySelector('.prompt-display').innerHTML = p.textContent;
                document.querySelector('#prompt-message-input').value = data.prompt;
            }
        };
    });
}

function disconnectChat() {
    if (chatSocket) {
        chatSocket.close();
    }
}


function selectPrompt(message, prompt, id, code, author) {
    if (chatSocket) {
        chatSocket.send(JSON.stringify({
            'message': message,
            'prompt': prompt,
            'facilitator_id': id,
            'code': code,
            'author': author,
            'save': false
        }));
    }
}

function sendChatMessage(message, prompt, id, code, author) {
    if (chatSocket) {
        chatSocket.send(JSON.stringify({
            'message': message,
            'prompt': prompt,
            'facilitator_id': id,
            'code': code,
            'author': author,
            'save': true
        }));
    }
}

function deleteChatMessage(message, prompt, id, code) {
    if (chatSocket) {
        chatSocket.send(JSON.stringify({
            'message': message,
            'prompt': prompt,
            'facilitator_id': id,
            'code': code
        }));
    }
}
// // Prompt
// function sendPrompt(prompt, id, code) {
//     if (chatSocket) {
//         chatSocket.send(JSON.stringify({
//             'prompt': prompt,
//             'facilitator_id': id,
//             'code': code
//         }));
//     }
// }
