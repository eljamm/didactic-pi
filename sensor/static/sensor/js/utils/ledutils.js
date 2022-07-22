function flipLED(led_id) {
    var led = document.getElementById(led_id);
    var id_list = String(led.classList).split('-');

    led.classList.remove(`${id_list.join('-')}`);

    if (id_list[2] === "inactive") {
        id_list[2] = "active";
    } else if ((id_list[2] === "active") && (id_list[1] !== "white")) {
        id_list[2] = "blink";
    } else {
        id_list[2] = "inactive";
    }

    led.classList.add(`${id_list.join('-')}`);
}

function constructMatrix(sensorName, x, y) {
    const x_array = [...Array(x).keys()];
    const y_array = [...Array(y).keys()];

    var leds = [];
    for (i in x_array) {
        var leds_temp = [];
        for (j in y_array) {
            var led = document.getElementById(`led-${i}-${j}`);
            var id_list = String(led.classList).split('-');
            
            if (sensorName === "8x8matrix") {
                if (id_list[2] === "active") {
                    leds_temp.push(0);
                } else {
                    leds_temp.push(1);
                }
            } else if (sensorName === "ledarray") {
                leds_temp.push(id_list[2]);
            }
        }
        leds.push(leds_temp);
    }
    return leds;
}

function updateMatrix(sensorName, x, y, leds) {
    const x_array = [...Array(x).keys()];
    const y_array = [...Array(y).keys()];

    for (i in x_array) {
        for (j in y_array) {
            var led = document.getElementById(`led-${i}-${j}`);
            var id_list = String(led.classList).split('-');

            led.classList.remove(`${id_list.join('-')}`);
            
            if (sensorName === "8x8matrix") {
                if (leds[i][j] === 0) {
                    id_list[2] = "active";
                } else {
                    id_list[2] = "inactive";
                }
            } else if (sensorName === "ledarray") {
                id_list[2] = leds[i][j];
            }
            
            led.classList.add(`${id_list.join('-')}`);
        }
    }
}

function clearLEDs(x, y) {
    const x_array = [...Array(x).keys()];
    const y_array = [...Array(y).keys()];

    for (i in x_array) {
        for (j in y_array) {
            var led = document.getElementById(`led-${i}-${j}`);
            var id_list = String(led.classList).split('-');
            led.classList.remove(`${id_list.join('-')}`);
            id_list[2] = "inactive";
            led.classList.add(`${id_list.join('-')}`);
        }
    }

    console.log("Cleared LEDs.");
}