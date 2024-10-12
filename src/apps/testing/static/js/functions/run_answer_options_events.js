import {AnswerOption} from "../classes/answer_option.js";


export function runAnswerOptionsEvents() {
    let taskName = $('[name="task_name"]').val();
    let answerOption = new AnswerOption(taskName);
    answerOption.triggerEvents();
}