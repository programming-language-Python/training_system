$(document).ready(function () {
    let $taskList = $("#task-list");
    const TIMEOUT = 500;

    putDownNumbering();

    // testing
    $("#btn-add-task-setup").click(blockTasks);

    // task
    $taskList.on("click", "[name = 'btn-update']", () => {
        setTimeout(putDownNumbering, TIMEOUT);
    });
    $taskList.on("click", ".btn-duplicate", () => {
        setTimeout(putDownNumbering, TIMEOUT);
    });
    $taskList.on("click", ".btn-delete", () => {
        setTimeout(putDownNumbering, TIMEOUT);
    });

    // task_form
    $taskList.on("click", ".btn-update", blockTasks);
    $taskList.on("click", "#task-form [name = 'btn-update']", unlockTasks);
    $taskList.on("click", "#btn-add", () => {
        unlockTasks()
        setTimeout(putDownNumbering, TIMEOUT);
    });

    function unlockTasks() {
        setTimeout(() => {
            let $error = document.getElementById('error');
            if (!$error) {
                const CLASS_DISABLED = 'disabled';
                $("[name='btns-testing']").removeClass(CLASS_DISABLED);
                $('.task').removeClass(CLASS_DISABLED);
                $(":input, a").attr("tabindex", "0");
                document.removeEventListener('keydown', _blockEnter);
            }
        }, TIMEOUT);
    }

    function blockTasks() {
        let classDisabled = 'disabled';
        $("[name='btns-testing']").addClass(classDisabled);
        $('.task').addClass(classDisabled);
        $(":input, a").attr("tabindex", "-1");
        document.addEventListener('keydown', _blockEnter);
    }

    function _blockEnter(event) {
        let isEnterPressed = event.keyCode === 13;
        if (isEnterPressed) {
            event.preventDefault();
        }
    }

    function putDownNumbering() {
        let $taskNumbers = document.querySelectorAll(".task-number"),
            numberTask = 1;
        for (let $taskNumber of $taskNumbers) {
            $taskNumber.textContent = numberTask.toString();
            numberTask++;
        }
        const COUNT = $taskNumbers.length;
        _updateCountTasks(COUNT)
    }

    function _updateCountTasks(count) {
        let $countTasks = $('#count-tasks');
        $countTasks.text(count.toString());
    }
})
