$(document).ready(function () {
    let duration = $('#duration').val();
    if (duration) {
        setTimeout(completeTesting, duration * 1000);
    }
});

function completeTesting() {
    $('#solving-testing-form').submit();
}
