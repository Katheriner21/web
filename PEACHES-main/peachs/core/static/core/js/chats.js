function iniciarChat(user, crv_id,users) {
    getOldMessages(crv_id);
    chats(users)

    console.log(user, crv_id)

    var url = 'ws://' + window.location.host + '/ws/crv/' + crv_id + '/' + user + '/'
    console.log(url)

    var chatSocket = new WebSocket(url);
    console.log(chatSocket)

    chatSocket.onopen = function (e) {
        console.log('WEBSOCKET ABIERTO')
    }

    chatSocket.onclose = function (e) {
        console.log('WEBSOCKET CERRADO')
    }

    chatSocket.onmessage = function (data) {
        const datamsj = JSON.parse(data.data)
        var msj = datamsj.message
        var datetime = datamsj.datetime

        document.querySelector('#boxMessages').innerHTML +=
            `
        <div class="message other-message" role="alert">
            ${msj}
            <div>
                <small class="float-end">${datetime}</small>
            </div>
        </div>
        `
        var boxMessages = document.querySelector('#boxMessages');
        boxMessages.scrollTop = boxMessages.scrollHeight;
    }

    document.querySelector('#btnMessage').addEventListener('click', sendMessage)
    document.querySelector('#inputMessage').addEventListener('keypress', function (e) {
        if (e.keyCode == 13) {
            sendMessage()
        }
    })


    function sendMessage() {
        var message = document.querySelector('#inputMessage')

        if (chatSocket.readyState === WebSocket.OPEN) {
            if (message.value.trim() !== '') {
                loadMessageHTML(message.value.trim());
                chatSocket.send(JSON.stringify({
                    message: message.value.trim(),
                }));
    
                console.log(message.value.trim());
    
                message.value = '';
            } else {
                console.log('Envió un mensaje vacío');
            }
        } else {
            console.log('La conexión WebSocket no está abierta');
            // Puedes intentar reconectar o mostrar un mensaje al usuario
        }
    }

    function loadMessageHTML(m) {

        var currentDatetime = new Date();
        var dateObject = new Date(currentDatetime)

        var year = dateObject.getFullYear();
        var month = ('0' + (dateObject.getMonth() + 1)).slice(-2);
        var day = ('0' + dateObject.getDate()).slice(-2);
        var hours = ('0' + dateObject.getHours()).slice(-2);
        var minutes = ('0' + dateObject.getMinutes()).slice(-2);
        var seconds = ('0' + dateObject.getSeconds()).slice(-2);

        const formattedDate = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`

        document.querySelector('#boxMessages').innerHTML +=
            `
        <div class="message my-message">
            ${m}
            <div>
                <small class="float-end">${formattedDate}</small>
            </div>
        </div>
        `
        var boxMessages = document.querySelector('#boxMessages');
        boxMessages.scrollTop = boxMessages.scrollHeight;
    }

    function getOldMessages(crvId) {
        // Realiza una solicitud AJAX para obtener mensajes antiguos desde el servidor
        $.get(`/get_old_messages/${crvId}/`, function (data) {
            data.forEach(function (messageData) {
                addMessageToChat(messageData.message, messageData.username, messageData.datetime);
            });
        });
    }

    function addMessageToChat(message, username, datetime) {
        var currentUser = user; // Suponiendo que `user` contiene el nombre de usuario actual

        var messageClass = (username === currentUser) ? 'my-message' : 'other-message';

        var messageHtml = `
            <div class="message ${messageClass}">
                <div>
                    <div>${message}</div>
                    <div>
                        <small class="float-end">${datetime}</small>
                    </div>
                </div>   
            </div>
        `;
        $('#boxMessages').append(messageHtml);
        msg();
    }

    function cerrarWebSocket() {
        chatSocket.close();
    }    

    function chats(user){
        var chatIcon = document.getElementById("chat-icon");
        var ClosechatIcon = document.getElementById("close-icon-chat2");
        var ClosechatIcon2 = document.getElementById("close-icon-chat3");
        var chatContainer = document.getElementById("chat-container");
        var chatContainer2 = document.getElementById("chat-container2");
    
        var h2Element = document.getElementById("userh2");
        h2Element.innerText = user;
    
        chatContainer2.style.display = "block";
        chatContainer.style.display = "none";
    
        ClosechatIcon.addEventListener("click", function(){
            chatContainer2.style.display = "none";
            chatIcon.style.display = "block";
        });
        ClosechatIcon2.addEventListener("click", function(){
            chatContainer2.style.display = "none";
            chatContainer.style.display = "block";
            boxMessages.innerHTML = "";
            cerrarWebSocket();
        });
    }
}

 function msg() {
    console.log('hola')
    var boxMessages = document.querySelector('#boxMessages');
    boxMessages.scrollTop = boxMessages.scrollHeight;
}