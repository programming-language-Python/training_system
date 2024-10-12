import '../../../../static/admin/js/vendor/jquery/jquery.js';
import {runAnswerOptionsEvents} from "./functions/run_answer_options_events.js";
import {changeCheckboxBehaviorToRadio} from "./functions/change_checkbox_behavior_to_radio.js";

$(document).ready(function () {
    runAnswerOptionsEvents();
    changeCheckboxBehaviorToRadio();
});
