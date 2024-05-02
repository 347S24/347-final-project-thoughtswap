console.log("socket.js loaded");

function connectChat(code) {
    return new Promise((resolve, reject) => {
        console.log('Connecting to chat...', code);
        let host = window.location.host
        // if (host.includes(':')){
        //     host = host.split(':')[0]
        //     host = host + ':6379'
        // }
        // console.log(host)
        chatSocket = new WebSocket(
            'ws://' + host +
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

            if (data.swap) {
                console.log('swap view');
                console.log('prompt', prompt)
                    let p = document.createElement('p');
                    p.textContent = data.prompt.trim();
                    document.querySelector('.prompt-display').innerHTML = p.textContent;
                    document.querySelector('#prompt-message-input').value = data.prompt;
            } else {
                if (data.message) {
                    console.log('message', data.message)
                    let div = document.createElement('div');
                    div.className = 'response-item';
                    div.innerHTML = data.message;
                    
                    // if no url, do not display delete button
                    if (deleteGroupUrl) {
                        console.log('fac view delete element')
                        let img = document.createElement('img');
                        img.src = "/static//media/trash-svgrepo-com.svg";
                        img.alt = 'delete thought';
                        
                        let btn = document.createElement('button');
                        btn.className = 'ud-button delete-thought';
                        // console.log(deleteGroupUrl)
                        // link.href = deleteGroupUrl;
                        btn.type = "button"
                        btn.onclick = deleteThought;
                        btn.appendChild(img);
        
                        let tip_container = document.createElement('div');
                        tip_container.className = 'tip-container';
                        tip_container.appendChild(btn);
                        div.appendChild(tip_container);
                    }
                    document.querySelector('#response-board').appendChild(div);
                }
                if (data.prompt) {
                    console.log('prompt', prompt)
                    let p = document.createElement('p');
                    p.textContent = data.prompt.trim();
                    document.querySelector('.prompt-display').innerHTML = p.textContent;
                    document.querySelector('#prompt-message-input').value = data.prompt;
                }
            }
        };
    });
}

function disconnectChat() {
    if (chatSocket) {
        chatSocket.close();
    }
}

function startSwap(code, fid) {
    if (chatSocket) {
        chatSocket.send(JSON.stringify({
            'message': 'Swap started',
            'prompt': prompt,
            'facilitator_id': fid,
            'code': code,
            'author': '',
            'save': false,
            'swap': true
        }));
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
            'save': false,
            'swap': false
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
            'save': true,
            'swap': false
        }));
    }
}


function sendSwapMessage(message, prompt, id, code, author) {
    if (chatSocket) {
        chatSocket.send(JSON.stringify({
            'message': message,
            'prompt': prompt,
            'facilitator_id': id,
            'code': code,
            'author': author,
            'save': true,
            'swap': true
        }));
    }
}

function deleteChatMessage(message, prompt, id, code, author) {
    if (chatSocket) {
        chatSocket.send(JSON.stringify({
            'message': message,
            'prompt': prompt,
            'facilitator_id': id,
            'code': code,
            'author': author,
            'save': false,
            'swap': false
        }));
    }
}

function deleteSwapMessage(message, prompt, id, code, author) {
    if (chatSocket) {
        chatSocket.send(JSON.stringify({
            'message': message,
            'prompt': prompt,
            'facilitator_id': id,
            'code': code,
            'author': author,
            'save': false,
            'swap': true
        }));
    }
}

function deleteThought(e) {
    const thought = e.target.parentElement.parentElement.parentElement.textContent.trim();
    const popup = document.getElementById("delete-popup");
    const span = document.getElementById("thought");
    span.innerText = thought;
    popup.classList.toggle("show-delete");
  }
