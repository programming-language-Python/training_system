export function changeCheckboxBehaviorToRadio() {
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