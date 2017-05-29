var card = document.getElementById('card');
var count = 0;

// https://stackoverflow.com/a/13328513/7435520
document.addEventListener('DOMContentLoaded', function () {
  if (!Notification) {
    alert('Desktop notifications not available in your browser. Try Chromium.');
    return;
  }

  if (Notification.permission !== "granted")
    Notification.requestPermission();
});

function notifyOver() {
  if (Notification.permission !== "granted")
    Notification.requestPermission();
  else {
    var notification = new Notification("Time's Up!", {
      icon: 'static/favicon.png',
      body: "Time to take a break from studying"
    });

    // notification.onclick = function () {
    //   window.open("http://stackoverflow.com/a/13328397/1269037");
    // };

  }

}

function formatTime(time) {
    var hours = Math.floor(time / 3600);
    if (hours < 10) {
        hours = "0" + hours;
    }
    time %= 3600;
    var minutes = Math.floor(time / 60);
    if (minutes < 10) {
        minutes = "0" + minutes;
    }
    var seconds = time % 60;
    if (seconds < 10) {
        seconds = "0" + seconds;
    }
    return hours + ":" + minutes + ":" + seconds;
}

function end() {
    notifyOver();
    navigator.vibrate = navigator.vibrate || navigator.webkitVibrate || navigator.mozVibrate || navigator.msVibrate;

    if ("vibrate" in navigator) {
        navigator.vibrate([500, 200, 100]);
    }

    var sound = document.getElementById("sound");
    sound.play();
    clearInterval(updateInterval);
}

function counter() {
    if (count <= timeRemaining) {
        if (count == workTime) {
            buttons = document.getElementById("buttons");
            buttons.style.visibility = "visible";
            update();
            end();
            return;
        }
        update();
        count += 1
    } else {
        end();
    }
}

function update() {
    // var percent = count / seconds * 100;
    // console.log(percent);
    var timeLeft = document.getElementById('time-left');
    timeLeft.innerHTML = formatTime(timeRemaining - count);

    // card.style.background = "linear-gradient(to right, #0000ff " + percent + "%,#0000ff 0%,#ff0000 0%,#ff0000 " + (100 - percent).toString + "%)";
}

var updateInterval = setInterval(counter, 1000);

function continueButton() {
    buttons = document.getElementById("buttons");
    buttons.style.visibility = "hidden";
    count += 1;
    updateInterval = setInterval(counter, 1000);
}

function nextButton() {
    window.location.href = '/work?time=' + count + '&next=' + next + 1;
}

