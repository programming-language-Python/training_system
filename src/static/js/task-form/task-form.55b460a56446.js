$(document).ready(function () {
    const TIMEOUT = 500;
    $("#task-list").on("click", ".btn-update", () => {
        setTimeout(blockOrUnblockFields, TIMEOUT);
    });
    $("#testing_by_code").on("click", "#btn-add-task", () => {
        setTimeout(blockOrUnblockFields, TIMEOUT);
    });

    function blockOrUnblockFields() {
        let $isIfOperator = $('#id_is_if_operator'),
            $conditionOfIfOperator = $('#id_condition_of_if_operator'),
            $cycle = $('#id_cycle'),
            $cycleCondition = $('#id_cycle_condition'),
            $operatorNesting = $('#id_operator_nesting'),
            $isOOP = $('#id_is_OOP'),
            $isStrings = $('#id_is_strings'),

            checkboxCycle = $cycle.find('input:checkbox'),

            valueIsIfOperator = $isIfOperator.val(),
            firstSelectValue = $isIfOperator.find('option:first').val(),
            isBePresent = valueIsIfOperator === firstSelectValue;
        const CLASS_DISABLED = "disabled";
        $('option[value=""]').hide();
        blockOrUnblockFields();

        function blockOrUnblockFields() {
            blockOrUnlockFieldOperatorNesting();
            blockOrUnblockFieldConditionOfIfOperator();
            blockOrUnblockFieldCycleCondition();
            if ($isOOP.is(':checked')) {
                blockOrUnlockAllFieldsExceptOne($isOOP);
            }
            $isOOP.click(() => blockOrUnlockAllFieldsExceptOne($isOOP));
            if ($isStrings.is(':checked')) {
                blockOrUnlockAllFieldsExceptOne($isStrings);
            }
            $isStrings.click(() => blockOrUnlockAllFieldsExceptOne($isStrings));
        }

        function blockOrUnlockFieldOperatorNesting() {
            let valueIsIfOperator = $isIfOperator.val(),
                firstSelectValue = $isIfOperator.find('option:first').val(),
                isIfOperator = valueIsIfOperator === firstSelectValue,
                checkbox_operator_nesting = $operatorNesting.find('input:checkbox');
            if (isIfOperator && checkboxCycle.is(':checked')) {
                unlock($operatorNesting)
                checkbox_operator_nesting.removeAttr(CLASS_DISABLED);
            } else {
                block($operatorNesting);
                checkbox_operator_nesting.attr(CLASS_DISABLED, true);
            }
        }

        function unlock(field) {
            field.parent().removeClass(CLASS_DISABLED);
        }

        function block(field) {
            field.parent().addClass(CLASS_DISABLED);
        }

        function blockOrUnblockFieldConditionOfIfOperator() {
            if (isBePresent) {
                unlock($conditionOfIfOperator);
            } else {
                block($conditionOfIfOperator);
            }
            $isIfOperator.change(() => {
                blockOrUnlock($conditionOfIfOperator);
                blockOrUnlockFieldOperatorNesting();
            });
            selectFirstOption($conditionOfIfOperator);
        }

        function blockOrUnlock(field) {
            field.parent().toggleClass(CLASS_DISABLED);
        }

        function selectFirstOption(select) {
            select.find('option:nth-child(2)').attr('selected', '');
        }

        function blockOrUnblockFieldCycleCondition() {
            if (checkboxCycle.is(':checked')) {
                unlock($cycleCondition);
            } else {
                block($cycleCondition);
            }
            checkboxCycle.click(() => {
                blockOrUnlockFieldOperatorNesting();
                if (checkboxCycle.is(':checked')) {
                    unlock($cycleCondition);
                } else {
                    block($cycleCondition);
                }
            })
        }

        function blockOrUnlockAllFieldsExceptOne($doNotBlockField) {
            $('.task__body div[id], .task__body select[id], .task__body input[id]').each(function (i, obj) {
                let $field = $('#' + obj.id),
                    isCycle = checkboxCycle.is(":checked"),
                    isContinue = obj.id === $doNotBlockField.attr('id')
                        || $field.is($cycleCondition) && !isCycle
                        || $field.is($conditionOfIfOperator) && !isBePresent;
                if (isContinue) {
                    return;
                }
                if ($field.parent().hasClass(CLASS_DISABLED)) {
                    unlock($field);
                } else {
                    block($field);
                }
            });
        }
    }
});
