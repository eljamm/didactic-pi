// --- Gauge Options --- //
var opts = {
    angle: 0.3,             // Span of the gauge arc
    lineWidth: 0.14,        // Line thickness
    radiusScale: 0.9,       // Relative radius
    pointer: {
        length: 0.6,        // Relative to gauge radius
        strokeWidth: 0.035, // The thickness
        color: "#000000",   // Fill color
    },
    limitMax: false,        // If false, max value increases automatically if value > maxValue
    limitMin: false,        // If true, the min value of the gauge will be fixed
    colorStart: "#000000",  // Colors
    colorStop: "#000000",
    strokeColor: "#D1D1D1",
    generateGradient: true,
    highDpiSupport: true,   // High resolution support
};

// --- Temperature Gauge --- //
var target = document.getElementById("temperaure");

// Modify colors
opts.colorStart = "#A01B1B";
opts.colorStop = "#DB1818";

var gauge_temp = new Donut(target).setOptions(opts);

// Temperature range: 0°C to 50°C
gauge_temp.maxValue = 50;
gauge_temp.setMinValue(0);
gauge_temp.animationSpeed = 32;
gauge_temp.set(25); // set start value
gauge_temp.setTextField(document.getElementById("temp-text"));


// --- Humidity Gauge --- //
var target = document.getElementById("humidity");

// Modify colors
opts.colorStart = "#120DB5";
opts.colorStop = "#6081DB";

var gauge_hum = new Donut(target).setOptions(opts);

// Humidity range: 20% to 90%
gauge_hum.maxValue = 90;
gauge_hum.setMinValue(20);
gauge_hum.animationSpeed = 32;
gauge_hum.set(35); // set start value
gauge_hum.setTextField(document.getElementById("humid-text"));

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
        console.log(data);

        // Process received data
        if (data.message_type === "data") {
            document.querySelector('#data-log').value += (data.message + '\n');

            var temp = document.getElementById('temp-text');
            var hum = document.getElementById('humid-text');

            // Set data values
            gauge_temp.set(data.temp);
            gauge_hum.set(data.hum);

            temp.textContent = data.temp;
            hum.textContent = data.hum;
        }
    };

    dataSocket.onopen = function (e) {
        // Send start signal
        dataSocket.send(JSON.stringify({
            'sensor': 'mt-' + sensorName,
            'message': 'start',
            'message_type': 'command'
        }));
    }

    window.onbeforeunload = function () {
        // Send stop signal
        dataSocket.send(JSON.stringify({
            'sensor': 'mt-' + sensorName,
            'message': 'stop',
            'message_type': 'command'
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
            'sensor': 'mt-' + sensorName,
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