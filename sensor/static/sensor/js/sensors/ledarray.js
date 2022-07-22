window.onload = function () {
    const piName = JSON.parse(document.getElementById('pi-name').textContent);
    const sensorName = JSON.parse(document.getElementById('sensor-name').textContent);

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
        var leds = data.message

        if (!data.sensor.match(/^mt-.*/i)) {
            updateMatrix(sensorName, 2, 10, leds)
        }

        console.log(data)
    };

    dataSocket.onopen = function (e) {
        dataSocket.send(JSON.stringify({
            'sensor': 'mt-' + sensorName,
            'message': 'start'
        }));
    }

    window.onbeforeunload = function () {
        dataSocket.send(JSON.stringify({
            'sensor': 'mt-' + sensorName,
            'message': 'stop'
        }));
        dataSocket.close
    };

    dataSocket.onclose = function (e) {
        console.error('Data socket closed unexpectedly');
    };

    document.querySelector('#send-data').onclick = function () {
        const message = constructMatrix(sensorName, 2, 10);
        dataSocket.send(JSON.stringify({
            'sensor': sensorName,
            'message': message
        }));
    };

    document.querySelector('#clear-data').onclick = function () {
        clearLEDs(2, 10);
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
            'sensor': sensorName,
            'message': message
        }));
        messageInputDom.value = '';
    };

    document.querySelector('#clear-textarea').onclick = function (e) {
        const dataLogDom = document.querySelector('#data-log');
        dataLogDom.value = '';
    };
}


