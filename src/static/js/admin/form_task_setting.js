$(document).ready(function () {
        let id_is_if_statement = $('#id_is_if_statement'),
            field_condition_of_if_statement = $('#id_condition_of_if_statement'),

            id_presence_one_of_following_cycles = $('#id_presence_one_of_following_cycles'),
            id_cycle_condition = $('#id_cycle_condition'),
            id_operator_nesting = $('#id_operator_nesting'),
            blocking_fields = []
        blocking_fields.push(id_cycle_condition, id_operator_nesting)
        remove_empty_options()
        block_or_unblock_field()

        function remove_empty_options() {
            $(field_condition_of_if_statement).find('option:first').remove()
            $(id_cycle_condition).find('option:first').remove()
        }

        function block_or_unblock_field() {
            block_or_unblock_field_select(id_is_if_statement, field_condition_of_if_statement)
            block_or_unblock_field_multiple_select(id_presence_one_of_following_cycles, blocking_fields)
        }

        function block_or_unblock_field_select(select, blocking_field) {
            let select_value = $(select).val(),
                first_select_value = $(select).find('option:first').val(),
                is_absent = select_value !== first_select_value
            if (is_absent)
                blocking_field.attr('disabled', true)
            select.change((event) => {
                if (event.target.value == first_select_value) {
                    blocking_field.removeAttr('disabled')
                } else
                    blocking_field.attr('disabled', true)
            })
        }

        function block_or_unblock_field_multiple_select(select, blocking_fields) {
            select.change(() => {
                    if (is_options_selected(select[0])) {
                        blocking_fields.forEach((blocking_field) => {
                            blocking_field.removeAttr('disabled')
                        })
                        return
                    }
                    blocking_fields.forEach((blocking_field) => {
                        blocking_field.attr('disabled', true)
                    })
                    return
                }
            )
        }

        function is_options_selected(select) {
            let result = [],
                options = select && select.options,
                opt
            for (let i = 0, iLen = options.length; i < iLen; i++) {
                opt = options[i]
                if (opt.selected)
                    result.push(opt.value || opt.text)
            }
            return result.length > 0
        }
    }
);
