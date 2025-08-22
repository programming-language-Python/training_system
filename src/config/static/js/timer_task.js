$(document).ready(function () {
    let $timeLeft = $('#id_time_left');
    let timeLeft = $timeLeft.val();
    let timeParts = timeLeft.split(':');
    let hours = parseInt(timeParts[0]);
    let minutes = parseInt(timeParts[1]);
    let seconds = parseInt(timeParts[2]);
    let totalSeconds = hours * 3600 + minutes * 60 + seconds;
    const timerInterval = setInterval(() => {
        totalSeconds--;
        let hours = Math.floor(totalSeconds / 3600);
        let minutes = Math.floor((totalSeconds % 3600) / 60);
        let seconds = totalSeconds % 60;
        $timeLeft.val(
            (hours < 10 ? '0' : '') + hours + ':' +
            (minutes < 10 ? '0' : '') + minutes + ':' +
            (seconds < 10 ? '0' : '') + seconds
        );
        if (totalSeconds <= 0) {
            clearInterval(timerInterval);
            $('#next-page').click();
        }
    }, 1000);
});
