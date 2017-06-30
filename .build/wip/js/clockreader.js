var x = document.getElementById("myRange").value;

var currentHour;
var currentMinute;

var minute;
var hour;


function startTime() {
    var today = new Date();
    var h = today.getHours();
    currentHour = h;
    var m = today.getMinutes();
    currentMinute = m;
    m = checkTime(m);
    document.getElementById('currenttime').innerHTML = "Current time: " + h + ":" + m;
    var t = setTimeout(startTime, 500);
    endTime();
};

function checkTime(i) {
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
};

// look for value of slider
function workTime() {
    console.log("hello")
    x = document.getElementById("myRange").value;
    var y = x * 5;
    minute = y % 60;
    hour = (y-minute)/60;

    minute = checkTime(minute);

    document.getElementById("worktime").innerHTML = "Working Time: " + hour + ":" + minute;
    endTime();
}

// update slider value

document.getElementById("myRange").addEventListener('onchange', workTime);



//output to "endtime" display
function endTime() {
    var a = parseInt(currentHour) + parseInt(hour);
    var b = parseInt(currentMinute) + parseInt(minute);
    if (b>60) {
      a += 1;
      b -= 60;
      b = checkTime(b);
    }
    if (a>=24) {
      a -= 24;
    }
    document.getElementById("endtime").innerHTML = "Estimated Finishing Time: " + a + ":" + b;
}

// COMMENTSSSSSSSS



/* Sources
 * https://www.w3schools.com/js/tryit.asp?filename=tryjs_timing_clock

*/
