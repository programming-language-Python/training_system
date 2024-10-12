import {setSerialNumbers, fitBlockToContentSize} from './functions/set_serial_numbers.js';

$(document).ready(function () {
    let $tasks = $('#tasks');
    fitBlockToContentSize();
    $tasks.on('DOMSubtreeModified', setSerialNumbers);
});
