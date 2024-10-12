$(document).ready(function () {
    let taskName = $('[name="task_name"]').val();
    let answerOption = new AnswerOption(taskName);
    let $answerOptions = $('#answer-options');
    answerOption.setSerialNumbers();
    answerOption.changeCheckboxBehaviorToRadio();
    $('#add-answer').click(() => answerOption.add());
    $answerOptions.on('click', '[data-name="delete"]', (event) => answerOption.delete(event));
    $answerOptions.on('DOMSubtreeModified', () => {
        answerOption.setSerialNumbers();
        let $answerOptions = $('[name="answer-option"]');
        for (let i = 0; i < $answerOptions.length; i++) {
            answerOption.setAttributes($($answerOptions[i]), i);
        }
    });
    answerOption.setQuantityAnswerOptionsAfterAdding();
    $('#quantity-add-answer-options').change(() => {
        answerOption.setQuantityAnswerOptionsAfterAdding();
    });
});

class AnswerOption {
    constructor(taskName) {
        this.taskName = taskName;
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

    setSerialNumbers() {
        let $serialNumbers = $('[data-name="serial-number"]');
        for (let i = 0; i < $serialNumbers.length; i++) {
            $serialNumbers[i].value = i + 1;
        }
        this._fitBlockToContentSize();
    }

    _fitBlockToContentSize() {
        let $serialNumbers = document.querySelectorAll('[data-is-fit-block-to-content-size="True"]');
        $serialNumbers.forEach((elem) => {
            elem.style.width = ((elem.value.length + 1) * 5) + 'px';
        });
    }

    changeCheckboxBehaviorToRadio() {
        $('#id_is_several_correct_answers').on('click', (event) => {
            let $isCorrectsChecked = $('[data-name="is-correct"]:checked');
            if (event.target.checked && $isCorrectsChecked.length === 1) {
                $('[data-name="is-correct"]:not(:checked)').first().prop('checked', true);
            } else {
                $('[data-name="is-correct"]').prop('checked', false);
                $isCorrectsChecked.first().prop('checked', true);
            }
        });
        $('#answer-options').on('click', '[data-name="is-correct"]', (event) => {
            if ($('#id_is_several_correct_answers').is(':checked')) {
                let $isCorrectsChecked = $('[data-name="is-correct"]:checked');
                if (!event.target.checked && $isCorrectsChecked.length < 2) {
                    event.target.checked = true;
                    alert('Вы выбрали "Допустимо несколько правильных ответов".\nС данной настройкой должны быть выбраны минимум 2 правильных вариантов ответа.');
                }
            } else {
                $('[data-name="is-correct"]').prop('checked', false);
                event.target.checked = true;
            }
        });
    }

    setQuantityAnswerOptionsAfterAdding() {
        let quantityAnswerOptions = $('[name="answer-option"]').length;
        let quantityAddAnswerOptions = Number($('#quantity-add-answer-options').val());
        let quantityAnswerOptionsAfterAdding = quantityAnswerOptions + quantityAddAnswerOptions;
        $('#quantity-answer-options-after-adding').val(quantityAnswerOptionsAfterAdding);
    }
}