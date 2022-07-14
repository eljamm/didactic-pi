const piName = JSON.parse(document.getElementById('pi-name').textContent);
const sensorName = JSON.parse(document.getElementById('sensor-name').textContent);

const dataSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + piName
    + '/'
);

dataSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data)
};

dataSocket.onclose = function (e) {
    console.error('Data socket closed unexpectedly');
};

document.querySelector('#data-message-input').focus();
document.querySelector('#data-message-input').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#data-message-submit').click();
    }
};

document.querySelector('#data-message-submit').onclick = function (e) {
    const messageInputDom = document.querySelector('#data-message-input');
    const message = messageInputDom.value;
    dataSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};
