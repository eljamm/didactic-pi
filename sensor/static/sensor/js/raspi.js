const sensorName = JSON.parse(document.getElementById('sensor-name').textContent);
const piName = JSON.parse(document.getElementById('pi-name').textContent);

const dataSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + piName
    + '/'
    + sensorName
    + '/'
);

dataSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    console.log(data)

    // Continuously add items
    config.data.labels.shift();
    config.data.labels.push(data.time.substring(11, 22));
    config.data.datasets[0].data.shift();
    config.data.datasets[0].data.push(data.message);
    myChart.update();
};

dataSocket.onclose = function (e) {
    console.error('Data socket closed unexpectedly');
    myChart.destroy()
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
