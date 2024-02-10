alert('Hi');
$(document).ready(function () {

    let $answerOptions = $('#answer-options');
    $answerOptions.on('DOMSubtreeModified', () => {
        setSerialNumbers();
    });
});

function setSerialNumbers() {
    let $serialNumbers = $('[data-name="serial-number"]');
    for (let i = 0; i < $serialNumbers.length; i++) {
        $serialNumbers[i].value = i + 1;
    }
    this._resizeSerialNumberInput();
}
