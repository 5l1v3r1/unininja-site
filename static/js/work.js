var card = document.getElementById('card');
var count = 0;

function update() {
    var percent = count / seconds * 100;
    console.log(percent);

    card.style.background = "linear-gradient(to right, #0000ff " + percent + "%,#0000ff 0%,#ff0000 0%,#ff0000 " + (100-percent).toString + "%)";
}

var updateInterval = setInterval(function () {
    if (count <= seconds) {
        update();
        count +=1
    } else {
        alert('done');
        clearInterval(updateInterval);
    }
}, 1000);