import {setSerialNumbers} from '../functions/set_serial_numbers.js';

export class AnswerOption {
    constructor(taskName) {
        this.taskName = taskName;
    }

    triggerEvents() {
        let $answerOptions = $('#answer-options');

        setSerialNumbers();
        $('#add-answer').click(() => this.add());
        $answerOptions.on('click', '[data-name="delete"]', (event) => this.delete(event));
        $answerOptions.on('DOMSubtreeModified', () => {
            setSerialNumbers();
            let $answerOptions = $('[name="answer-option"]');
            for (let i = 0; i < $answerOptions.length; i++) {
                this.setAttributes($($answerOptions[i]), i);
            }
        });
        $('#quantity-add-answer-options').change(() => {
            this.setQuantityAnswerOptionsAfterAdding();
        });
    }

    add() {
        let $answerOptions = $('[name="answer-option"]');
        let $newAnswerOption = $answerOptions.first().clone();
        let quantity = $answerOptions.length;
        $newAnswerOption.find('[data-name="is-correct"]').prop('checked', false);
        $(`#id_${this.taskName}_related-TOTAL_FORMS`).val(quantity + 1);
        $newAnswerOption = this.setAttributes($newAnswerOption, quantity);
        $('[name="answer-options"]').append($newAnswerOption);
    }

    setAttributes($answerOption, index) {
        let firstSubstringName = `${this.taskName}_answer_option_set-`;
        let firstSubstringId = "id_" + firstSubstringName;
        $answerOption.find('[data-name="serial-number"]')
            .attr('name', firstSubstringName + index + '-serial_number')
            .attr('id', firstSubstringId + index + '-serial_number');
        $answerOption.find('[data-name="description"]')
            .attr('name', firstSubstringName + index + '-description')
            .attr('id', firstSubstringId + index + '-description');
        $answerOption.find('[data-name="is-correct"]')
            .attr('name', firstSubstringName + index + '-is_correct')
            .attr('id', firstSubstringId + index + '-is_correct');
        $answerOption.find('[data-name="delete"]')
            .attr('name', firstSubstringName + index + '-DELETE')
            .attr('id', firstSubstringId + index + '-DELETE');
        $answerOption.find('[data-name="closed-question"]')
            .attr('name', `${firstSubstringId}${index}-${this.taskName}`)
            .attr('id', `${firstSubstringId}${index}-${this.taskName}`);
        return $answerOption;
    }

    delete(event) {
        let quantityAnswerOptions = $('[name="answer-option"]').length;
        let quantitySelectedDeletions = $('[data-name="delete"]:checked').length;
        if (quantityAnswerOptions - quantitySelectedDeletions < 2) {
            alert('Вы не можете удалить данный ответ. Минимальное допустимое количество ответов 2.');
            $(event.target).prop('checked', false);
        }
    }

    setQuantityAnswerOptionsAfterAdding() {
        let quantityAnswerOptions = $('[name="answer-option"]').length;
        let quantityAddAnswerOptions = Number($('#quantity-add-answer-options').val());
        let quantityAnswerOptionsAfterAdding = quantityAnswerOptions + quantityAddAnswerOptions;
        $('#quantity-answer-options-after-adding').val(quantityAnswerOptionsAfterAdding);
    }
}