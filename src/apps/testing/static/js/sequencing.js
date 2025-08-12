import '/static/admin/js/vendor/jquery/jquery.js';
import {AnswerOption} from "./classes/answer_option.js";
import {setSerialNumbers} from '/static/js/set_serial_numbers.js';

class SequencingAnswerOption extends AnswerOption {
    triggerEvents() {
        let $answerOptions = $('#answer-options');
        let $correctOptions = $('#correct-options');
        let $incorrectOptions = $('#incorrect-options');
        let options = {
            attributes: true,
            childList: true,
        };
        const observer = new MutationObserver((mutations) => {
            setSerialNumbers();
            let $answerOptions = $('[name="answer-option"]');
            for (let i = 0; i < $answerOptions.length; i++) {
                this.setAttributes($($answerOptions[i]), i);
            }
        });
        const observerAnswerOptions = new MutationObserver((mutations) => {
            this.triggerEvents();
        });

        observer.observe($correctOptions[0], options);
        observer.observe($incorrectOptions[0], options);
        observerAnswerOptions.observe($answerOptions[0], options);

        setSerialNumbers();
        $('#add-answer').click(() => this.add());
        $answerOptions.on('click', '[data-name="delete"]', (event) => this.delete(event));

        $('#quantity-add-answer-options').change(() => {
            this.setQuantityAnswerOptionsAfterAdding();
        });
    }

    moveOptions() {
        $('#answer-options li[name="answer-option"]').each(function () {
            let checkbox = $(this).find('input[type="checkbox"][name$="is_correct"]');
            if (checkbox.length && checkbox.prop('checked')) {
                $('#correct-options').append(this);
            } else {
                $('#incorrect-options').append(this);
            }
        });
    }
}

$(document).ready(function () {
    let sequencingAnswerOption = new SequencingAnswerOption();
    sequencingAnswerOption.triggerEvents();

    $(document).on('change', 'input[type="checkbox"][name$="is_correct"]', function () {
        sequencingAnswerOption.moveOptions();
    });
});
