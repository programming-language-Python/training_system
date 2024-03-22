$(document).ready(function () {
    let $tasks = $('#tasks');
    resizeSerialNumberInput();
    $tasks.on('DOMSubtreeModified', setSerialNumbers);
});

function setSerialNumbers() {
    let $serialNumbers = $('[data-name="serial-number"]');
    for (let i = 0; i < $serialNumbers.length; i++) {
        $serialNumbers[i].value = i + 1;
    }
    resizeSerialNumberInput();
}

function resizeSerialNumberInput() {
    let $serialNumbers = document.querySelectorAll('[data-name="serial-number"]');
    $serialNumbers.forEach((elem) => {
        elem.style.width = ((elem.value.length + 1) * 5) + 'px';
    });
}
