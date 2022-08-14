window.onload = function () {
    const debug = JSON.parse(document.getElementById('debug').textContent);
    const piName = JSON.parse(document.getElementById('pi-name').textContent);
    const sensorName = JSON.parse(document.getElementById('sensor-name').textContent);
    const extraFunction = JSON.parse(document.getElementById('extra-function').textContent);

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

        // Process received data
        if (data.message_type === "data") {
            document.querySelector('#data-log').value += (data.message + '\n');
        }
    };

    dataSocket.onopen = function () {
        // Send start signal
        dataSocket.send(JSON.stringify({
            'sensor': sensorName + `-${extraFunction}`,
            'message': 'start',
            'message_type': 'command'
        }));
    }

    window.onbeforeunload = function () {
        // Send stop signal
        dataSocket.send(JSON.stringify({
            'sensor': sensorName + `-${extraFunction}`,
            'message': 'stop',
            'message_type': 'command'
        }));
        dataSocket.close
    };

    dataSocket.onclose = function () {
        console.error('Data socket closed unexpectedly');
    };

    // -- Control Buttons --
    if (extraFunction === "alarm") {
        document.querySelector('#send-data').addEventListener('click', () => {
            dataSocket.send(JSON.stringify({
                'sensor': sensorName,
                'message': "play",
                'message_type': 'data'
            }));
        });

        document.querySelector('#clear-data').addEventListener('click', () => {
            dataSocket.send(JSON.stringify({
                'sensor': sensorName,
                'message': "stop",
                'message_type': 'data'
            }));
        });
    } else if (extraFunction === "midi") {
        const fired_list = [];

        const midi_keys = [
            "w",
            "x", "s", "c", "d", "v", "f", "b",
            "n", "j", ",", "k", ";",
            "a", "é", "z", "\"", "e", "'", "r",
            "t", "-", "y", "è", "u"
        ];

        document.addEventListener('keydown', (e) => {
            if (midi_keys.includes(e.key)) {
                if (!fired_list.includes(e.key)) {
                    fired_list.push(e.key);

                    dataSocket.send(JSON.stringify({
                        'sensor': sensorName,
                        'message': "play-" + e.key,
                        'message_type': 'data'
                    }));
                }
            }
        });

        document.addEventListener('keyup', (e) => {
            if (midi_keys.includes(e.key)) {
                if (fired_list.includes(e.key)) {
                    const index = fired_list.indexOf(e.key);
                    fired_list.splice(index, 1);

                    if (fired_list.length === 0) {
                        dataSocket.send(JSON.stringify({
                            'sensor': sensorName,
                            'message': "stop",
                            'message_type': 'data'
                        }));
                    }
                }
            }
        });
    }

    // -- Debug --
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
                'sensor': sensorName + `-${extraFunction}`,
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