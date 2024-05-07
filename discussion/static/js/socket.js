console.log("socket.js loaded");

function connectChat(code, user) {
    return new Promise((resolve, reject) => {
        console.log('Connecting to chat...', code);
        // let host = window.location.host
        console.log('user is:', user)
        // chatSocket = new WebSocket(
        //     'ws://' + host +
        //     '/ws/discussion/' + code + '/'
        // );
        var websocketURL = ((location.protocol == 'https:') ? "wss" : "ws") + "://" + window.location.host + '/ws/discussion/' + code + '/';

        chatSocket = new ReconnectingWebSocket(websocketURL);
        console.log('chatsocket', chatSocket)

        chatSocket.addEventListener('open', () => {
            resolve(chatSocket);
        });

        chatSocket.addEventListener('error', () => {
            reject(new Error("Failed to connect"));
        });

        chatSocket.addEventListener('message', (e) => {
            const data = JSON.parse(e.data);
            console.log('data', data)
            console.log('data', data.swap)
            console.log('thoughts', data.thoughts)

            if (data.swap) {
                // Get participant and assign the new, swapped thought
                console.log('Swapping thought', data.swap, "with user", author)
                if (data.swap[author]) {
                    console.log('swap[user]', data.swap[author])
                    let container = document.querySelector('.swap-display');
                    let response_container = document.querySelector('.participant-response');
                    let div = document.querySelector('#distributed-thought');
                    div.innerHTML = data.swap[author];
                    container.classList.toggle('show-swap-response');
                    response_container.classList.toggle('show-swap-response');
                }
            } else if (data.save == false && data.prompt == '') {
                // Delete Thought
                console.log("deleting thought", data.message)
                let parent = document.querySelector('.response');
                let children = document.querySelectorAll('.response-item');
                children.forEach(function (child) {
                    if (child.textContent.trim() == data.message.trim()) {
                        parent.removeChild(child);
                    }
                });
            } else {
                // Display a message
                if (data.message) {
                    console.log('Sending message', data.message)
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
                    parent = document.querySelector('#response-board')
                    parent.insertBefore(div, parent.children[1]);
                }
                // Display a prompt and it's thoughts
                if (data.prompt) {
                    console.log('Sending prompt', prompt)
                    let p = document.createElement('p');
                    p.textContent = data.prompt.trim();
                    document.querySelector('.prompt-display').innerHTML = p.textContent;
                    let input = document.querySelector('#prompt-message-input')
                    if (input) {
                        input.value = data.prompt;
                    }
                }
                // Display thoughts
                console.log('Displaying thoughts', data.thoughts)
                var parent = document.querySelector('#response-board');
                while (parent.children.length > 1) {
                    parent.removeChild(parent.lastChild);
                }
                let thoughts = Object.values(data.thoughts);
                if (thoughts) {
                    thoughts.forEach(function (thought) {
                        let div = document.createElement('div');
                        div.className = 'response-item';
                        div.innerHTML = thought;
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
                        document.querySelector('.response').appendChild(div);
                    });
                }
            }
        });
    });
}

function disconnectChat() {
    if (chatSocket) {
        chatSocket.close();
    }
}

function startSwap(code, fid, prompt) {
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
    // let parent_board = e.target.parentElement.parentElement;
    // let item = e.target.parentElement.parentElement.parentElement;
    const thought = e.target.parentElement.parentElement.parentElement.textContent.trim();
    const popup = document.getElementById("delete-popup");
    const span = document.getElementById("thought");
    span.innerText = thought;
    popup.classList.toggle("show-delete");
    // parent_board.removeChild(item);
}
