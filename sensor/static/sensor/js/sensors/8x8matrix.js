window.onload = function () {
    const debug = JSON.parse(document.getElementById('debug').textContent);
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
        console.log(data);

        var leds = data.message;

        // Don't log control messages to the debugging textfield
        if (!data.message_type === "command") {
            updateMatrix(sensorName, 8, 8, leds);
        }
    };

    dataSocket.onopen = function (e) {
        dataSocket.send(JSON.stringify({
            'sensor': sensorName,
            'message': 'start',
            'message_type': 'command'
        }));
    }

    window.onbeforeunload = function () {
        dataSocket.send(JSON.stringify({
            'sensor': sensorName,
            'message': 'stop',
            'message_type': 'command'
        }));
        dataSocket.close
    };

    dataSocket.onclose = function (e) {
        console.error('Data socket closed unexpectedly');
    };

    document.querySelector('#send-data').onclick = function () {
        const message = constructMatrix(sensorName, 8, 8);
        dataSocket.send(JSON.stringify({
            'sensor': sensorName,
            'message': message,
        }));
    };

    document.querySelector('#clear-data').onclick = function () {
        clearLEDs(8, 8);
    };

    if (debug === true) {
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
                'message': message,
                'message_type': 'command'
            }));
            messageInputDom.value = '';
        };

        document.querySelector('#clear-textarea').onclick = function (e) {
            const dataLogDom = document.querySelector('#data-log');
            dataLogDom.value = '';
        };
    }
}
