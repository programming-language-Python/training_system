$(document).ready(function () {
    let answerOption = new AnswerOption();
    let $answerOptions = $('#answer-options');
    answerOption.setSerialNumbers();
    answerOption.changeCheckboxBehaviorToRadio();

    $('#add-answer').click(() => answerOption.add());
    $answerOptions.on('click', '[name="btn-delete"]', (event) => answerOption.delete(event));
    $answerOptions.on('DOMSubtreeModified', () => answerOption.setSerialNumbers());
    $answerOptions.change('.photo', (event) => answerOption.showImage(event));
});

class AnswerOption {
    add() {
        let $answerOptions = $('[name="answer-option"]');
        let $newAnswerOption = $answerOptions.first().clone();
        let quantity = $answerOptions.length;
        $newAnswerOption.find('.is-correct').prop('checked', false);
        $('#id_form-TOTAL_FORMS').val(quantity + 1);
        $newAnswerOption = this._setAttributes($newAnswerOption, quantity);
        $('[name="answer-options"]').append($newAnswerOption);
    }

    _setAttributes($answerOption, index) {
        $answerOption.find('.serial-number')
            .attr('name', 'form-' + index + '-serial_number')
            .attr('id', 'id_form-' + index + '-serial_number');
        $answerOption.find('textarea')
            .attr('name', 'form-' + index + '-description')
            .attr('id', 'id_form-' + index + '-description');
        $answerOption.find('input[type="file"]')
            .attr('name', 'form-' + index + '-photo')
            .attr('id', 'id_form-' + index + '-photo');
        $answerOption.find('input[type="checkbox"]')
            .attr('name', 'form-' + index + '-is_correct')
            .attr('id', 'id_form-' + index + '-is_correct');
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
                this._setAttributes($answerOption, index);
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
        let $serialNumbers = $('.serial-number');
        for (let i = 0; i < $serialNumbers.length; i++) {
            $serialNumbers[i].value = i + 1;
        }
        this._resizeSerialNumberInput();
    }

    _resizeSerialNumberInput() {
        let $serialNumbers = document.querySelectorAll('.serial-number');
        $serialNumbers.forEach((elem) => {
            elem.style.width = ((elem.value.length + 1) * 4) + 'px';
        });
    }

    changeCheckboxBehaviorToRadio() {
        $('.is-correct').first().prop('checked', true);
        $('#answer-options').on('click', '.is-correct', (event) => {
            if (!$('#id_is_several_correct_answers').is(':checked')) {
                $('.is-correct').prop('checked', false);
                event.target.checked = true;
            }
        });
    }
}