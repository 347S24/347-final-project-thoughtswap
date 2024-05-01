console.log("socket.js loaded");
<<<<<<< HEAD
// same socket across pages ?
=======
>>>>>>> channels

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
<<<<<<< HEAD
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
=======

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
>>>>>>> channels
            }
        };
    });
}

function disconnectChat() {
    if (chatSocket) {
        chatSocket.close();
    }
}

<<<<<<< HEAD

function selectPrompt(message, prompt, id, code) {
=======
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
>>>>>>> channels
    if (chatSocket) {
        chatSocket.send(JSON.stringify({
            'message': message,
            'prompt': prompt,
            'facilitator_id': id,
            'code': code,
<<<<<<< HEAD
            'save': false
=======
            'author': author,
            'save': false,
            'swap': false
>>>>>>> channels
        }));
    }
}

<<<<<<< HEAD
function sendChatMessage(message, prompt, id, code) {
=======
function sendChatMessage(message, prompt, id, code, author) {
>>>>>>> channels
    if (chatSocket) {
        chatSocket.send(JSON.stringify({
            'message': message,
            'prompt': prompt,
            'facilitator_id': id,
            'code': code,
<<<<<<< HEAD
            'save': true
=======
            'author': author,
            'save': true,
            'swap': false
>>>>>>> channels
        }));
    }
}

<<<<<<< HEAD
function deleteChatMessage(message, prompt, id, code) {
=======

function sendSwapMessage(message, prompt, id, code, author) {
>>>>>>> channels
    if (chatSocket) {
        chatSocket.send(JSON.stringify({
            'message': message,
            'prompt': prompt,
            'facilitator_id': id,
<<<<<<< HEAD
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
=======
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
>>>>>>> channels
