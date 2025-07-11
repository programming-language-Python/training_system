import {setSerialNumbers, fitBlockToContentSize} from './set_serial_numbers.js';

$(document).ready(function () {
    const $tasks = $('#task-list');
    fitBlockToContentSize();

    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            setSerialNumbers();
        });
    });

    observer.observe($tasks[0], {
        childList: true,
    });
});
