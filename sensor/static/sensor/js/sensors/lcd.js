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

        // Don't log control messages to the debugging textfield
        if (!data.message_type === "command") {
            document.querySelector('#lcd-data-log').value += (data.message + '\n');
        }
    };

    dataSocket.onopen = function (e) {
        dataSocket.send(JSON.stringify({
            'sensor': `mt-${sensorName}`,
            'message': 'start',
            'message_type': 'command'
        }));
    }

    window.onbeforeunload = function () {
        dataSocket.send(JSON.stringify({
            'sensor': `mt-${sensorName}`,
            'message': 'stop',
            'message_type': 'command'
        }));
        dataSocket.close
    };

    dataSocket.onclose = function (e) {
        console.error('Data socket closed unexpectedly');
    };

    document.querySelector('#lcd-data-message-input').onkeyup = function (e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#lcd-data-message-submit').click();
        }
    };

    document.querySelector('#lcd-data-message-submit').onclick = function (e) {
        const messageInputDom = document.querySelector('#lcd-data-message-input');
        const message = messageInputDom.value;
        dataSocket.send(JSON.stringify({
            'sensor': sensorName,
            'message': message,
            'message_type': 'data'
        }));
        messageInputDom.value = '';
    };

    document.querySelector('#lcd-clear-textarea').onclick = function (e) {
        const dataLogDom = document.querySelector('#lcd-data-log');
        dataLogDom.value = '';
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
                'sensor': `mt-${sensorName}`,
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


