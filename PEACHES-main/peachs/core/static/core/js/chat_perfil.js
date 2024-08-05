document.addEventListener("DOMContentLoaded", function() {
    var chatIcon = document.getElementById("chat-icon");
    var ClosechatIcon = document.getElementById("close-icon-chat");
    var chatContainer = document.getElementById("chat-container");

    chatIcon.addEventListener("click", function() {
        chatContainer.style.display = "block";
        chatIcon.style.display = "none";
        var boxMessages = document.querySelector('#boxMessages');
        boxMessages.scrollTop = boxMessages.scrollHeight;
    });

    ClosechatIcon.addEventListener("click", function(){
        chatContainer.style.display = "none";
        chatIcon.style.display = "block";
    });
});