window.onload = function () {
    const debug = JSON.parse(document.getElementById('debug').textContent);
    const piName = JSON.parse(document.getElementById('pi-name').textContent);
    const sensorName = JSON.parse(document.getElementById('sensor-name').textContent);
    const extraFunction = JSON.parse(document.getElementById('extra-function').textContent);
    
    if (extraFunction === "gauge") {
        var [gauge_temp, gauge_hum] = createGauge();
    };

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

            if (extraFunction === "gauge") {
                var temp = document.getElementById('temp-text');
                var hum = document.getElementById('humid-text');

                // Set data values
                gauge_temp.set(data.temp);
                gauge_hum.set(data.hum);

                temp.textContent = data.temp;
                hum.textContent = data.hum;
            }
        }
    };

    dataSocket.onopen = function (e) {
        // Send start signal
        dataSocket.send(JSON.stringify({
            'sensor': sensorName+`-${extraFunction}`,
            'message': 'start',
            'message_type': 'command'
        }));
    }

    window.onbeforeunload = function () {
        // Send stop signal
        dataSocket.send(JSON.stringify({
            'sensor': sensorName+`-${extraFunction}`,
            'message': 'stop',
            'message_type': 'command'
        }));
        dataSocket.close
    };

    dataSocket.onclose = function (e) {
        console.error('Data socket closed unexpectedly');
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
                'sensor': sensorName+`-${extraFunction}`,
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