var assignmentButton = document.getElementById('assignment-add');
var examButton = document.getElementById('exam-add');
var taskButton = document.getElementById('task-add');

var buttons = [assignmentButton, examButton, taskButton];
var taskTypes = ['assignment', 'exam', 'task'];


function work() {
    var workSeconds = $("#slider").roundSlider("getValue") * 5 * 60;
    document.location = "work?time=" + workSeconds;
}

taskTypes.forEach(function (type) {
    updateDueTime(type);
})

function updateDueTime(type) {
    var indate = document.getElementById('new-' + type + '-date').value.split("/");
    var intime = document.getElementById('new-' + type + '-time').value.split(":");

    var realDate = new Date(indate[2], indate[1] - 1, indate[0], intime[0], intime[1]);

    var realDateInput = document.getElementById("new-" + type + "-due_time").value = realDate.getTime() / 1000 | 0;
}

function updateSlider(id, type) {
    var slider = document.getElementById('new-' + type + '-' + id);
    var parrot = document.getElementById(type + '-' + id + '-parrot');
    parrot.innerHTML = String(slider.value);
}

function updateTask(id) {
    var slider = document.getElementById('task' + id + "slider");
    var parrot = document.getElementById('task' + id);
    parrot.innerHTML = String(slider.value);
}

function updateComplete(id, type) {
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
        getTasks(type);
    });
}

function newTask(type) {
    var headerLogo = document.getElementById("header-logo");
    headerLogo.style.animation = "spin 1s infinite linear";

    var getData = {
        "name": document.getElementById("new-" + type + "-name").value,
        "subject": document.getElementById("new-" + type + "-subject").value,
        "details": document.getElementById("new-" + type + "-details").value,
        "type": type,
        "due_time": document.getElementById("new-" + type + "-due_time").value,
        "percent_worth": document.getElementById("new-" + type + "-worth").value,
        "percent_complete": document.getElementById("new-" + type + "-complete").value
    };

    $.getJSON('new', getData, function (data) {
        if (data['status'] == 'failure') {
            headerLogo.style.animation = "";
            return;
        }
        headerLogo.style.animation = "";
    });
}

taskTypes.forEach(function (type) {
    updateSlider('worth', type);
    updateSlider('complete', type);
});


for (var i = 0; i < taskTypes.length; i++) {
    var button = buttons[i];
    var taskType = taskTypes[i];

    button.addEventListener("click", function (e) {
        var taskType = e.target.id.split('-')[0];
        // Toggle cards
        var cards = Array.from(document.getElementsByClassName(taskType + "-card"));
        cards.forEach(function (card) {
            card.style.display = card.style.display == "none" ? "block" : "none";
        });

        // Toggle icon
        var icon = document.getElementById(taskType + "-i");
        icon.innerHTML = icon.innerHTML == "add" ? "check" : "add";

        // Toggle form
        var spacers = Array.from(document.getElementsByClassName("new-" + taskType + "-spacer"));
        spacers.forEach(function (spacer) {
            $(spacer).toggle();
        });

        var form = document.getElementById("new-" + taskType);
        $(form).toggle();

        if (icon.innerHTML == "add") {
            getTasks(taskType);
        }

    });
}


taskTypes.forEach(function (type) {
    getTasks(type);
});

function getTasks(type) {
    var headerLogo = document.getElementById("header-logo");
    headerLogo.style.animation = "spin 1s infinite linear";
    var getData = {
        'type': type
    };


    $.getJSON('tasks', getData, function (data) {
        if (data['status'] == 'failure') {
            return;
        }

        var oldCards = Array.from(document.getElementsByClassName(type + "-card"));
        oldCards.forEach(function (card) {
            card.remove()
        });

        var tasks = data['tasks'];

        var taskBadge = document.getElementById(type + '-badge');
        console.log("setting styles");
        taskBadge.setAttribute("data-badge", tasks.length);
        taskBadge.classList.remove('hidden-badge');

        for (i = 0; i < tasks.length; i++) {
            createCard(tasks[i], type);
        }
        headerLogo.style.animation = "";
    });
}

function createCard(task, type) {
    var typeDiv = document.getElementById(type + "s");

    var cardDiv = document.createElement('div');
    cardDiv.classList.add("mdl-card");
    cardDiv.classList.add("mdl-shadow--2dp");
    cardDiv.classList.add(type + "-card");

    var titleDiv = document.createElement('div');
    titleDiv.classList.add("mdl-card__title");
    titleDiv.style.backgroundColor = task["color"];

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
    percentCompleteSlider.setAttribute("onchange", "updateComplete('" + task['id'] + "', '" + type + "')");


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
    var offset = new Date().getTimezoneOffset() * 60000;
    t = new Date(t.getTime() - offset);
    var formatted = t.toString().slice(0, 21);

    dueDateDiv.innerHTML = "Due Date: " + formatted;

    cardDiv.appendChild(dueDateDiv);

    var buttonDiv = document.createElement('div');
    buttonDiv.classList.add("mdl-card__actions");
    buttonDiv.classList.add("mdl-card--border");

    var spacerDiv = document.createElement('div');
    spacerDiv.classList.add('mdl-layout-spacer');

    var deleteButton = document.createElement('i');
    deleteButton.classList.add("material-icons");
    deleteButton.innerHTML = "delete";

    buttonDiv.appendChild(spacerDiv);
    buttonDiv.appendChild(deleteButton);
    cardDiv.appendChild(buttonDiv);

    typeDiv.appendChild(cardDiv);
    if (!(typeof(componentHandler) == 'undefined')) {
        componentHandler.upgradeAllRegistered();
    }
}