$(document).ready(function () {
    const TIMEOUT = 500;
    $("#task-list").on("click", ".btn-update", () => {
        setTimeout(blockOrUnblockFields, TIMEOUT);
    });
    $("#testing").on("click", "#btn-add-task", () => {
        setTimeout(blockOrUnblockFields, TIMEOUT);
    });

    function blockOrUnblockFields() {
        let $isIfOperator = $('#id_is_if_operator'),
            $conditionOfIfOperator = $('#id_condition_of_if_operator'),
            $presenceOneOfCycles = $('#id_presence_one_of_cycles'),
            $cycleCondition = $('#id_cycle_condition'),
            $operatorNesting = $('#id_operator_nesting'),
            $isOOP = $('#id_is_OOP'),
            $isStrings = $('#id_is_strings');
        const CLASS_DISABLED = "disabled";
        $('option[value=""]').hide();
        blockOrUnblockFields();

        function blockOrUnblockFields() {
            blockOrUnlockFieldOperatorNesting();
            blockOrUnblockFieldConditionOfIfOperator();
            blockOrUnblockFieldCycleCondition();
            blockOrUnlockFieldsDependingOnConditionAndCycle();
        }

        function blockOrUnlockFieldOperatorNesting() {
            let valueIsIfOperator = $isIfOperator.val(),
                firstSelectValue = $isIfOperator.find('option:first').val(),
                isIfOperator = valueIsIfOperator === firstSelectValue,
                checkboxPresenceOneOfCycles = $presenceOneOfCycles.find('input:checkbox'),
                isPresenceOneOfCycles = checkboxPresenceOneOfCycles.is(":checked"),
                checkbox_operator_nesting = $operatorNesting.find('input:checkbox');
            if (isIfOperator && isPresenceOneOfCycles) {
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
            let valueIsIfOperator = $isIfOperator.val(),
                firstSelectValue = $isIfOperator.find('option:first').val(),
                is_be_present = valueIsIfOperator === firstSelectValue;
            if (is_be_present) {
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
            let checkboxPresenceOneOfCycles = $presenceOneOfCycles.find('input:checkbox')
            if (checkboxPresenceOneOfCycles.is(':checked')) {
                unlock($cycleCondition);
            } else {
                block($cycleCondition);
            }
            checkboxPresenceOneOfCycles.click(() => {
                blockOrUnlockFieldOperatorNesting();
                if (checkboxPresenceOneOfCycles.is(':checked')) {
                    unlock($cycleCondition);
                } else {
                    block($cycleCondition);
                }
            })
        }

        function blockOrUnlockFieldsDependingOnConditionAndCycle() {
            let valueIsIfOperator = $isIfOperator.val(),
                firstSelectValue = $isIfOperator.find('option:first').val(),
                isIfOperator = valueIsIfOperator === firstSelectValue,

                checkboxPresenceOneOfCycles = $presenceOneOfCycles.find('input:checkbox'),
                isPresenceOneOfCycles = checkboxPresenceOneOfCycles.is(":checked"),

                isBlock = isIfOperator || isPresenceOneOfCycles;
            if (isBlock) {
                blockFieldsDependingOnConditionAndCycle();
            } else {
                unlockFieldsDependingOnConditionAndCycle();
            }
            checkboxPresenceOneOfCycles.click(() => {
                let valueIsIfOperator = $isIfOperator.val(),
                    isIfOperator = valueIsIfOperator === firstSelectValue;
                if (isIfOperator || checkboxPresenceOneOfCycles.is(':checked')) {
                    blockFieldsDependingOnConditionAndCycle();
                } else {
                    unlockFieldsDependingOnConditionAndCycle();
                }
            });
            $isIfOperator.change(() => {
                let valueIsIfOperator = $isIfOperator.val(),
                    isIfOperator = valueIsIfOperator === firstSelectValue;
                if (isIfOperator) {
                    blockFieldsDependingOnConditionAndCycle();
                } else {
                    unlockFieldsDependingOnConditionAndCycle();
                }
            });
        }

        function blockFieldsDependingOnConditionAndCycle() {
            block($isOOP);
            block($isStrings);
        }

        function unlockFieldsDependingOnConditionAndCycle() {
            unlock($isOOP);
            unlock($isStrings);
        }
    }
});
