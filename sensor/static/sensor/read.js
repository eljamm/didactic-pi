const sensorName = JSON.parse(document.getElementById('sensor-name').textContent);

const dataSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/sensor/read/'
    + sensorName
    + '/'
);

dataSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    document.querySelector('#data-log').value += (data.message + '\n');
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

function showLoc() {
    var oLocation = location, aLog = ["Property (Typeof): Value", "location (" + (typeof oLocation) + "): " + oLocation];
    for (var sProp in oLocation) {
        aLog.push(sProp + " (" + (typeof oLocation[sProp]) + "): " + (oLocation[sProp] || "n/a"));
    }
    alert(aLog.join("\n"));
}
