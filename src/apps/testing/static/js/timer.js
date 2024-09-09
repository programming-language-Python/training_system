$(document).ready(function () {
    let duration = $('#duration').val();
    setTimeout(completeTesting, duration * 1000);
});

function completeTesting() {
    $('#solving-testing-form').submit();
}
