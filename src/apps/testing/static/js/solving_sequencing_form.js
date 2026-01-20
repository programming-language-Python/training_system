$(function () {
    const $correctOptions = $('#correct-options');
    const $incorrectOptions = $('#incorrect-options');

    // сортировка <li> в правильные варианты ответы и не правильные
    const moveLi = ($li, $targetUl) => {
        if ($li.parent().is($targetUl)) return;
        $li.appendTo($targetUl);
    };

    $('li[name="answer-option"]').each(function () {
        const $li = $(this);
        const $checkbox = $li.find('input[type="checkbox"]');
        const isCorrect = $checkbox.length && $checkbox.is(':checked');
        moveLi($li, isCorrect ? $correctOptions : $incorrectOptions);
    });

    $(document).on('change', 'li[name="answer-option"] input[type="checkbox"]', function () {
        const $li = $(this).closest('li[name="answer-option"]');
        const isCorrect = $(this).is(':checked');
        moveLi($li, isCorrect ? $correctOptions : $incorrectOptions);
    });
});
