$(document).ready(function () {
    let $leadTime = $('#id_lead_time');
    blockOrUnlockTaskLeadTime($leadTime.val());
    $leadTime.change((e) => {
        blockOrUnlockTaskLeadTime(e.target.value);
    });
});

function blockOrUnlockTaskLeadTime(valueLeadTime) {
    let $taskLeadTime = $('#id_task_lead_time');
    if (valueLeadTime) {
        $taskLeadTime.prop('readonly', true);
        $taskLeadTime.addClass('block');
    } else {
        $taskLeadTime.prop('readonly', false);
        $taskLeadTime.removeClass('block');
    }
}