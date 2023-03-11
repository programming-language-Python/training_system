$(document).ready(function () {
        $("[name='btn-update']").click(() => {
            setTimeout(block_or_unblock_fields, 1000)
        })
        $('#btn-add-task-setup').click(() => {
            setTimeout(block_or_unblock_fields, 1000)
        })

        function block_or_unblock_fields() {
            let id_is_if_operator = $('#id_is_if_operator'),
                id_condition_of_if_operator = $('#id_condition_of_if_operator'),
                id_presence_one_of_cycles = $('#id_presence_one_of_cycles'),
                id_cycle_condition = $('#id_cycle_condition'),
                id_operator_nesting = $('#id_operator_nesting'),
                blocking_fields = []
            $('option[value=""]').hide()
            blocking_fields.push(id_cycle_condition, id_operator_nesting)
            block_or_unblock_field()

            function block_or_unblock_field() {
                block_or_unblock_field_select(id_is_if_operator, id_condition_of_if_operator)
                id_presence_one_of_cycles.change(() => {
                    block_or_unblock_field_multiple_select(id_presence_one_of_cycles)
                    select_first_option(id_cycle_condition)
                }, block_or_unblock_field_multiple_select(id_presence_one_of_cycles))
            }

            function block_or_unblock_field_select(select, blocking_field) {
                let select_value = $(select).val(),
                    first_select_value = $(select).find('option:first').val(),
                    is_absent = select_value !== first_select_value
                if (is_absent)
                    block_field_select(blocking_field)
                select.change((event) => {
                    if (event.target.value === first_select_value) {
                        unblock_field_select(blocking_field)
                        select_first_option(id_condition_of_if_operator)
                    } else
                        block_field_select(blocking_field)
                    block_or_unblock_field_multiple_select(id_operator_nesting)
                })
            }

            function select_first_option(select) {
                select.find('option:nth-child(2)').attr('selected', '')
            }

            function block_field_select(blocking_field) {
                let selected_value = $(blocking_field).val(),
                    selected_value_blog = $(blocking_field).find('option[value="' + selected_value + '"]')
                selected_value_blog.val('')
                blocking_field.attr('disabled', true)
            }

            function unblock_field_select(blocking_field) {
                let selected_value = $(blocking_field).val(),
                    selected_value_blog = $(blocking_field)
                        .find('option[value="' + selected_value + '"]:not([style])'),
                    selected_text_blog = selected_value_blog.text()
                selected_value_blog.val(selected_text_blog)
                blocking_field.removeAttr('disabled')
            }


            function block_or_unblock_field_multiple_select(multiple_select) {
                blocking_fields.forEach((blocking_field) => {
                    if (is_options_selected(multiple_select[0]))
                        unblock_field_select(blocking_field)
                    else
                        block_field_select(blocking_field)
                })
            }

            function is_options_selected(multiple_select) {
                let result = [],
                    options = multiple_select && multiple_select.options,
                    opt
                for (let i = 0, iLen = options.length; i < iLen; i++) {
                    opt = options[i]
                    if (opt.selected)
                        result.push(opt.value || opt.text)
                }
                return result.length > 0
            }

            function block_or_unlock_operator_nesting() {
                id_presence_one_of_cycles.change(()=>{

                })
            }
        }
    }
);
