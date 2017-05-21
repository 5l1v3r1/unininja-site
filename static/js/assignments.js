var assignmentButton = document.getElementById('assignment-add');
var examButton = document.getElementById('exam-add');
var taskButton = document.getElementById('task-add');

function updateSlider(id) {
    var slider = document.getElementById('new-assignment-' + id);
    var parrot = document.getElementById(id + '-parrot');
    parrot.innerHTML = String(slider.value);
}

updateSlider('worth');
updateSlider('complete');


assignmentButton.addEventListener("click", function () {
    // Toggle cards
    var cards = Array.from(document.getElementsByClassName("assignment-card"));
    cards.forEach(function (card) {
        card.style.display = card.style.display == "none" ? "block" : "none";

    });

    // Toggle icon
    var icon = document.getElementById("assignment-i");
    icon.innerHTML = icon.innerHTML == "add" ? "check" : "add";

    // Toggle form
    var spacers = Array.from(document.getElementsByClassName("new-assignment-spacer"));
    spacers.forEach(function (spacer) {
        $(spacer).toggle();
    });

    var form = document.getElementById("new-assignment");
    $(form).toggle();
});


