$(document).ready(function () {
    $("[name='btn-update']").click(() => {
        let class_disabled = 'disabled'
        $("[name='btns-testing']").addClass(class_disabled)
        $('.task').addClass(class_disabled)

        $(document).keydown(function (event) {
            let keycode1 = (event.keyCode ? event.keyCode : event.which);
            if (keycode1 === 0 || keycode1 === 9) {
                event.preventDefault();
                event.stopPropagation();
            }
        })
    })
})