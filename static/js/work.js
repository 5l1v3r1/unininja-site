var card = document.getElementById('card');
var count = 0;

function formatTime(time) {
    var hours = Math.floor(time / 3600);
    if (hours < 10){
        hours = "0" + hours;
    }
    time %= 3600;
    var minutes = Math.floor(time / 60);
    if (minutes < 10){
        minutes = "0" + minutes;
    }
    var seconds = time % 60;
    if (seconds < 10){
        seconds = "0" + seconds;
    }
    return hours + ":" + minutes + ":" + seconds;
}

function update() {
    // var percent = count / seconds * 100;
    // console.log(percent);
    var timeLeft = document.getElementById('time-left');
    timeLeft.innerHTML = formatTime(timeRemaining - count);

    // card.style.background = "linear-gradient(to right, #0000ff " + percent + "%,#0000ff 0%,#ff0000 0%,#ff0000 " + (100 - percent).toString + "%)";
}

var updateInterval = setInterval(function () {
    if (count <= timeRemaining) {
        update();
        count += 1
    } else {
        navigator.vibrate = navigator.vibrate || navigator.webkitVibrate || navigator.mozVibrate || navigator.msVibrate;

        if ("vibrate" in navigator) {
            navigator.vibrate([500, 200, 100]);
        }

        var sound = document.getElementById("sound");
        sound.play();
        clearInterval(updateInterval);
    }
}, 1000);