export function setSerialNumbers() {
    let $serialNumbers = $('[data-name="serial-number"]');
    for (let i = 0; i < $serialNumbers.length; i++) {
        $serialNumbers[i].value = i + 1;
    }
    fitBlockToContentSize();
}

export function fitBlockToContentSize() {
    let $serialNumbers = document.querySelectorAll('[data-is-fit-block-to-content-size="True"]');
    $serialNumbers.forEach((elem) => {
        elem.style.width = ((elem.value.length + 1) * 5) + 'px';
    });
}