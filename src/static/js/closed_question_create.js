$(document).ready(function () {
    let answerOption = new AnswerOption();
    let $answerOptions = $('#answer-options');
    answerOption.setSerialNumbers();
    answerOption.changeCheckboxBehaviorToRadio();
    $('#add-answer').click(() => answerOption.add());
    $answerOptions.on('click', '[name="btn-delete"]', (event) => answerOption.delete(event));
    $answerOptions.on('DOMSubtreeModified', () => {
        answerOption.setSerialNumbers();
        let $answerOptions = $('[name="answer-option"]');
        for (let i = 0; i < $answerOptions.length; i++) {
            answerOption.setAttributes($($answerOptions[i]), i);
        }
    });
    $answerOptions.change('[data-name="photo"]', (event) => answerOption.showImage(event));
});

class AnswerOption {
    add() {
        let $answerOptions = $('[name="answer-option"]');
        let $newAnswerOption = $answerOptions.first().clone();
        let quantity = $answerOptions.length;
        $newAnswerOption.find('[data-name="is-correct"]').prop('checked', false);
        $('#id_closed_question_related-TOTAL_FORMS').val(quantity + 1);
        $newAnswerOption = this.setAttributes($newAnswerOption, quantity);
        $('[name="answer-options"]').append($newAnswerOption);
    }

    setAttributes($answerOption, index) {
        let firstSubstringName = 'closed_question_related-';
        let firstSubstringId = "id_" + firstSubstringName;
        $answerOption.find('[data-name="serial-number"]')
            .attr('name', firstSubstringName + index + '-serial_number')
            .attr('id', firstSubstringId + index + '-serial_number');
        $answerOption.find('[data-name="description"]')
            .attr('name', firstSubstringName + index + '-description')
            .attr('id', firstSubstringId + index + '-description');
        $answerOption.find('input[type="file"]')
            .attr('name', firstSubstringName + index + '-photo')
            .attr('id', firstSubstringId + index + '-photo');
        $answerOption.find('[data-name="is-correct"]')
            .attr('name', firstSubstringName + index + '-is_correct')
            .attr('id', firstSubstringId + index + '-is_correct');
        $answerOption.find('[data-name="delete"]')
            .attr('name', firstSubstringName + index + '-DELETE')
            .attr('id', firstSubstringId + index + '-DELETE');
        $answerOption.find('[data-name="id"]')
            .attr('name', firstSubstringName + index + '-id')
            .attr('id', firstSubstringId + index + '-id');
        $answerOption.find('[data-name="closed-question"]')
            .attr('name', firstSubstringName + index + '-closed_question')
            .attr('id', firstSubstringId + index + '-closed_question');
        return $answerOption;
    }

    delete(event) {
        let quantityAnswerOptions = $('[name="answer-option"]').length;
        if (quantityAnswerOptions > 2) {
            let $answerOption = event.target.closest('[name="answer-option"]');
            $answerOption.remove();
            quantityAnswerOptions--;
            for (let index = 0; index < quantityAnswerOptions; index++) {
                let $answerOption = $($('[name="answer-option"]')[index]);
                this.setAttributes($answerOption, index);
            }
        } else {
            alert('Вы не можете удалить ответ. Минимальное количество ответов 2.');
        }
    }

    showImage(event) {
        let $inputFile = event.target;
        if ($inputFile.files && $inputFile.files[0]) {
            let reader = new FileReader();
            reader.onload = function (e) {
                let $newImg = $('<img>', {
                    'src': e.target.result,
                    'uk-img': true
                });
                let $parent = $($inputFile).parent();
                let $img = $parent.find('img');
                let $imgInput = $parent.find('> [name="img-input"]');
                if ($img.length) {
                    $imgInput.val($inputFile.files[0].name);
                    $img.replaceWith($newImg);
                } else {
                    $imgInput.after($newImg);
                }
            }
            reader.readAsDataURL($inputFile.files[0]);
        }
    }

    setSerialNumbers() {
        let $serialNumbers = $('[data-name="serial-number"]');
        for (let i = 0; i < $serialNumbers.length; i++) {
            $serialNumbers[i].value = i + 1;
        }
        this._resizeSerialNumberInput();
    }

    _resizeSerialNumberInput() {
        let $serialNumbers = document.querySelectorAll('[data-name="serial-number"]');
        $serialNumbers.forEach((elem) => {
            elem.style.width = ((elem.value.length + 1) * 4) + 'px';
        });
    }

    changeCheckboxBehaviorToRadio() {
        $('[data-name="is-correct"]').first().prop('checked', true);
        $('#answer-options').on('click', '[data-name="is-correct"]', (event) => {
            if (!$('#id_is_several_correct_answers').is(':checked')) {
                $('[data-name="is-correct"]').prop('checked', false);
                event.target.checked = true;
            }
        });
    }
}