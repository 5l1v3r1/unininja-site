var assignmentButton = document.getElementById('assignment-add');
var examButton = document.getElementById('exam-add');
var taskButton = document.getElementById('task-add');

updateDueTime();

function updateDueTime() {
    var indate = document.getElementById('new-assignment-date').value.split("/");
    var intime = document.getElementById('new-assignment-time').value.split(":");

    var realDate = new Date(indate[2], indate[1]-1, indate[0], intime[0], intime[1]);

    var realDateInput = document.getElementById("new-assignment-due_time").value = realDate.getTime()/1000|0;
}

function updateSlider(id) {
    var slider = document.getElementById('new-assignment-' + id);
    var parrot = document.getElementById(id + '-parrot');
    parrot.innerHTML = String(slider.value);
}

function updateTask(id) {
    var slider = document.getElementById('task' + id + "slider");
    var parrot = document.getElementById('task' + id);
    parrot.innerHTML = String(slider.value);
}

function updateComplete(id) {
    var headerLogo = document.getElementById("header-logo");
    headerLogo.style.animation = "spin 1s infinite linear";

    var value = document.getElementById("task" + id + "slider").value;

    var getData = {
        "id": id,
        "value": value
    };

    $.getJSON('update', getData, function (data) {
        if (data['status'] == 'failure') {
            return;
        }
        headerLogo.style.animation = "";
    });
}

function newAssignment() {
    var headerLogo = document.getElementById("header-logo");
    headerLogo.style.animation = "spin 1s infinite linear";

    var getData = {
        "name": document.getElementById("new-assignment-name").value,
        "subject": document.getElementById("new-assignment-subject").value,
        "details": document.getElementById("new-assignment-details").value,
        "type": "assignment",
        "due_time": document.getElementById("new-assignment-due_time").value,
        "percent_worth": document.getElementById("new-assignment-worth").value,
        "percent_complete": document.getElementById("new-assignment-complete").value
    };
    console.log(getData);

    $.getJSON('new', getData, function (data) {
        if (data['status'] == 'failure') {
            return;
        }
        headerLogo.style.animation = "";
    });
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

var types = ['assignment', 'exam', 'task'];

types.forEach(function (type) {
    getTasks(type);
});

function getTasks(type) {
    var getData = {
        'type': type
    };

    $.getJSON('tasks', getData, function (data) {
        if (data['status'] == 'failure') {
            return;
        }
        var tasks = data['tasks'];
        for (var i = 0; i < tasks.length; i++) {
            createCard(tasks[i], type);
        }
    });
}

function createCard(task, type) {
    var typeDiv = document.getElementById(type + "s");

    var cardDiv = document.createElement('div');
    cardDiv.classList.add("mdl-card");
    cardDiv.classList.add("mdl-shadow--2dp");
    cardDiv.classList.add("assignment-card");

    var titleDiv = document.createElement('div');
    titleDiv.classList.add("mdl-card__title");

    var titleParagraph = document.createElement('h4');
    titleParagraph.innerHTML = "<strong>" + task['subject'] + "</strong> " + task['name'];

    titleDiv.appendChild(titleParagraph);
    cardDiv.appendChild(titleDiv);

    var detailsDiv = document.createElement('div');
    detailsDiv.classList.add("mdl-card__actions");
    detailsDiv.classList.add("mdl-card--border");
    detailsDiv.classList.add("mdl-card--expand");
    detailsDiv.innerHTML = "Details:<p>" + task['details'] + "</p>";

    cardDiv.appendChild(detailsDiv);

    var percentCompleteDiv = document.createElement('div');
    percentCompleteDiv.classList.add("mdl-card__actions");
    percentCompleteDiv.classList.add("mdl-card--border");
    percentCompleteDiv.innerHTML = "<span id='task" + task['id'] + "'>" + task['percent_complete'] + "</span>% Complete";

    var percentCompleteSlider = document.createElement("input");
    percentCompleteSlider.classList.add("mdl-slider");
    percentCompleteSlider.classList.add("mdl-js-slider");
    percentCompleteSlider.setAttribute("type", "range");
    percentCompleteSlider.setAttribute("min", "0");
    percentCompleteSlider.setAttribute("max", "100");
    percentCompleteSlider.setAttribute("tabindex", "0");
    percentCompleteSlider.setAttribute("value", task['percent_complete']);
    percentCompleteSlider.setAttribute("id", "task" + task['id'] + "slider");
    percentCompleteSlider.setAttribute("oninput", "updateTask('" + task['id'] + "')");
    percentCompleteSlider.setAttribute("onchange", "updateComplete('" + task['id'] + "')");


    percentCompleteDiv.appendChild(percentCompleteSlider);
    cardDiv.appendChild(percentCompleteDiv);

    var test = document.createElement('div');
    test.classList.add("mdl-card__actions");
    test.classList.add("mdl-card--border");
    test.innerHTML = task['percent_worth'] + "% of Grade";

    var percentWorthSlider = document.createElement("input");
    percentWorthSlider.classList.add("mdl-slider");
    percentWorthSlider.classList.add("mdl-js-slider");
    percentWorthSlider.setAttribute("type", "range");
    percentWorthSlider.setAttribute("min", "0");
    percentWorthSlider.setAttribute("max", "100");
    percentWorthSlider.setAttribute("tabindex", "0");
    percentWorthSlider.setAttribute("value", task['percent_worth']);
    percentWorthSlider.disabled = true;

    test.appendChild(percentWorthSlider);
    cardDiv.appendChild(test);

    var dueDateDiv = document.createElement('div');
    dueDateDiv.classList.add("mdl-card__actions");
    dueDateDiv.classList.add("mdl-card--border");
    var t = new Date(task['due_time'] * 1000);
    var formatted = t.toString().slice(0, 24);
    dueDateDiv.innerHTML = "Due Date: " + formatted;

    cardDiv.appendChild(dueDateDiv);

    var buttonDiv = document.createElement('div');
    buttonDiv.classList.add("mdl-card__actions");
    buttonDiv.classList.add("mdl-card--border");

    var spacerDiv = document.createElement('div');
    spacerDiv.classList.add('mdl-layout-spacer');

    var editButton = document.createElement('i');
    editButton.classList.add("material-icons");
    editButton.innerHTML = "edit";

    var deleteButton = document.createElement('i');
    deleteButton.classList.add("material-icons");
    deleteButton.innerHTML = "delete";

    buttonDiv.appendChild(spacerDiv);
    buttonDiv.appendChild(editButton);
    buttonDiv.appendChild(deleteButton);
    cardDiv.appendChild(buttonDiv);

    typeDiv.appendChild(cardDiv);
    if (!(typeof(componentHandler) == 'undefined')) {
        componentHandler.upgradeAllRegistered();
    }
}