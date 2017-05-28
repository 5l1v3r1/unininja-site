var currentHour;
var currentMinute;

function startTime() {
    var today = new Date();
    var h = today.getHours();
    currentHour = h;
    var m = today.getMinutes();
    currentMinute = m;
    m = checkTime(m);
    document.getElementById('currentTime').innerHTML = "It's currently: " + h + ":" + m;
    var t = setTimeout(startTime, 500);
    workTime();
    endTime();
}

function checkTime(i) {
    if (i < 10) {// add zero in front of numbers < 10
        i = "0" + i;
    }
    return i;
}

//output to "endtime" display
function endTime() {
    var a = parseInt(currentHour) + parseInt(hour);
    var b = parseInt(currentMinute) + parseInt(minute);
    if (b >= 60) {
        a += 1;
        b -= 60;
        b = checkTime(b);
    }
    if (b < 10 && parseInt(currentMinute) < 10) {
        b = checkTime(b);
    }
    if (a > 24) {
        a -= 24;
    }
    document.getElementById("endTime").innerHTML = "I'll be done at: " + a + ":" + b;
}

function workTime() {
    x = $("#slider").roundSlider("getValue");
    var y = x * 5;
    minute = y % 60;
    hour = (y - minute) / 60;

    // minute = checkTime(minute);

    if (hour == 0) {
        document.getElementById("workTime").innerHTML = "I can work for " + minute + " minutes";
    } else if (hour == 1) {
        if (minute == 0) {
            document.getElementById("workTime").innerHTML = "I can work for an hour";
        } else {
            document.getElementById("workTime").innerHTML = "I can work for an hour and " + minute + " minutes";
        }
    } else {
        if (minute == 0) {
            document.getElementById("workTime").innerHTML = "I can work for " + hour + " hours";
        } else {
            document.getElementById("workTime").innerHTML = "I can work for " + hour + " hours and " + minute + " minutes";
        }
    }

    // document.getElementById("working_time").value = y * 60;
    endTime();
}

function initSlider() {
    $("#slider").roundSlider({
        handleShape: "dot",
        width: 25,
        radius: 100,
        value: 42,
        circleShape: "pie",
        startAngle: 315,
        showTooltip: false,
        sliderType: "min-range",
        handleSize: "+10",
        max: "60",
        drag: function () {
            workTime();
        },
        create: function () {
            $('.rs-inner.rs-bg-color.rs-border').css("background-color", "#424242");
            $('.rs-overlay.rs-transition.rs-bg-color').css("background-color", "#424242");
        }
    });
}

