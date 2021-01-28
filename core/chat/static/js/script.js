document.getElementById("send-button").onclick = function (e) {
    const chatHistory = document.getElementById("chat-history")
    const messageInputDom = document.getElementById("input")
    const message = messageInputDom.value
    const receiver = chatHistory.getAttribute("data-contact")
    console.log(receiver)
    message != "" ? 
    chatSocket.send(JSON.stringify({
        "message": message,
        "username": username,
        "receiver": receiver,
        "action": "send"
    })) : {}

    messageInputDom.value = ""
}

function deleteMessage(id){
    chatSocket.send(JSON.stringify({
        "id": id,
        "action": "delete"
    }))
}


var wsScheme = window.location.protocol == "https:" ? "wss" : "ws"
const chatSocket = new WebSocket(
    wsScheme +
    "://" +
    window.location.host +
    "/ws/chat/" +
    roomHash + 
    "/"
)

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data)
    const chatHistory = document.getElementById("chat-history")
    const action = data.action
    const toastSender = document.getElementById("toast-sender")
    const toastMessage = document.getElementById("toast-message")
    const toast = $("#toast")



    if (action !== "delete" && data.sender !== username){
        toastSender.innerHTML = data.sender
        toastMessage.innerHTML = data.message
        toast.toast("show", {
            delay: 50000
        })
    }

    action !== "delete" ? 
    
        chatHistory.innerHTML += data.sender !== username ?  
        `<div class="incoming_msg" id=${data.id}>
            <div class="incoming_msg_img"> <img src="https://ptetutorials.com/images/user-profile.png" alt="sunil"> </div>
            <div class="received_msg">
            <div class="received_withd_msg">
                <p>${data.message}</p>
                <span class="time_date">${data.timestamp}</span><i style="color: red; cursor: pointer;" onclick="deleteMessage(${data.id})" class="fa fa-trash"></i></div>
            </div>
        </div>` 
        : 
        `<div class="outgoing_msg" id=${data.id}>
        <div class="sent_msg">
        <p>${data.message}</p>
        <span class="time_date">${data.timestamp}</span><i style="color: red; cursor: pointer;" onclick="deleteMessage(${data.id})" class="fa fa-trash"></i></div>
    </div>`

    :
    

  
    document.getElementById(data.id)
        .remove()
} 

