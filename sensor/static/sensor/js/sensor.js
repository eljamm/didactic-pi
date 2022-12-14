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

        if (!data.message_type === "command") {
            document.querySelector('#data-log').value += (data.message + '\n');
        }

        console.log(data)

        if (sensorName === 'dht11') {
            const temp = document.getElementById('temp-text')
            const hum = document.getElementById('humid-text')

            gauge_temp.set(data.temp);
            gauge_hum.set(data.hum);

            temp.textContent = data.temp;
            hum.textContent = data.hum;
        }
    };

    dataSocket.onopen = function (e) {
        dataSocket.send(JSON.stringify({
            'sensor': sensorName,
            'message': 'start'
        }));
    }

    window.onbeforeunload = function () {
        dataSocket.send(JSON.stringify({
            'sensor': sensorName,
            'message': 'stop'
        }));
        dataSocket.close
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


