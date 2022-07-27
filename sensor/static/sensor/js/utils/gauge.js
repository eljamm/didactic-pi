function createGauge() {
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

    // Humidity range: 10% to 90%
    gauge_hum.maxValue = 90;
    gauge_hum.setMinValue(10);
    gauge_hum.animationSpeed = 32;
    gauge_hum.set(35); // set start value
    gauge_hum.setTextField(document.getElementById("humid-text"));

    return [gauge_temp, gauge_hum];
}