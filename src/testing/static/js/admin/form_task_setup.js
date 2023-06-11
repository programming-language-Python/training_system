$(document).ready(function () {
        $("[name='btn-update']").click(() => {
            setTimeout(block_or_unblock_fields, 1000)
        })
        $('#btn-add-task-setup').click(() => {
            setTimeout(block_or_unblock_fields, 1000)
        })

        function block_or_unblock_fields() {
            let $is_if_operator = $('#id_is_if_operator'),
                $condition_of_if_operator = $('#id_condition_of_if_operator'),
                $presence_one_of_cycles = $('#id_presence_one_of_cycles'),
                $cycle_condition = $('#id_cycle_condition'),
                $operator_nesting = $('#id_operator_nesting')
            $('option[value=""]').hide()
            block_or_unblock_fields()

            function block_or_unblock_fields() {
                block_or_unlock_field_operator_nesting()
                block_or_unblock_field_condition_of_if_operator()
                block_or_unblock_field_cycle_condition()
            }

            function block_or_unlock_field_operator_nesting() {
                let value_is_if_operator = $is_if_operator.val(),
                    first_select_value = $is_if_operator.find('option:first').val(),
                    is_if_operator = value_is_if_operator === first_select_value,
                    checkbox_presence_one_of_cycles = $presence_one_of_cycles.find('input:checkbox'),
                    is_presence_one_of_cycles = checkbox_presence_one_of_cycles.is(":checked"),
                    checkbox_operator_nesting = $operator_nesting.find('input:checkbox')
                if (is_if_operator && is_presence_one_of_cycles) {
                    unlock($operator_nesting)
                    checkbox_operator_nesting.removeAttr('disabled')
                } else {
                    block($operator_nesting)
                    checkbox_operator_nesting.attr('disabled', true)
                }
            }

            function unlock(field) {
                field.parent().removeClass('disabled')
            }

            function block(field) {
                field.parent().addClass('disabled')
            }

            function block_or_unblock_field_condition_of_if_operator() {
                let value_is_if_operator = $is_if_operator.val(),
                    first_select_value = $is_if_operator.find('option:first').val(),
                    is_be_present = value_is_if_operator === first_select_value
                if (is_be_present)
                    unlock($condition_of_if_operator)
                else
                    block($condition_of_if_operator)
                $is_if_operator.change(() => {
                    block_or_unlock($condition_of_if_operator)
                    block_or_unlock_field_operator_nesting()
                })
                select_first_option($condition_of_if_operator)
            }

            function block_or_unlock(field) {
                field.parent().toggleClass('disabled')
            }

            function select_first_option(select) {
                select.find('option:nth-child(2)').attr('selected', '')
            }

            function block_or_unblock_field_cycle_condition() {
                let checkbox_presence_one_of_cycles = $presence_one_of_cycles.find('input:checkbox')
                if (checkbox_presence_one_of_cycles.is(':checked'))
                    unlock($cycle_condition)
                else
                    block($cycle_condition)
                checkbox_presence_one_of_cycles.click(() => {
                    block_or_unlock_field_operator_nesting()
                    if (checkbox_presence_one_of_cycles.is(':checked'))
                        unlock($cycle_condition)
                    else
                        block($cycle_condition)
                })
            }
        }
    }
);

//
// $(document).ready(function () {
//         $("[name='btn-update']").click(() => {
//             setTimeout(block_or_unblock_fields, 1000)
//         })
//         $('#btn-add-task-setup').click(() => {
//             setTimeout(block_or_unblock_fields, 1000)
//         })
//
//         function block_or_unblock_fields() {
//             let id_is_if_operator = $('#id_is_if_operator'),
//                 id_condition_of_if_operator = $('#id_condition_of_if_operator'),
//                 $presence_one_of_cycles = $('#id_presence_one_of_cycles'),
//                 $cycle_condition = $('#id_cycle_condition'),
//                 $operator_nesting = $('#id_operator_nesting'),
//                 blocking_fields = []
//             $('option[value=""]').hide()
//             blocking_fields.push($cycle_condition, $operator_nesting)
//             block_or_unblock_field()
//
//             function block_or_unblock_field() {
//                 block_or_unblock_field_select(id_is_if_operator, id_condition_of_if_operator)
//                 $presence_one_of_cycles.change(() => {
//                     alert('dd')
//                     block_or_unblock_field_multiple_select($presence_one_of_cycles)
//                     select_first_option($cycle_condition)
//                 }, block_or_unblock_field_multiple_select($presence_one_of_cycles))
//             }
//
//             function block_or_unblock_field_select(select, blocking_field) {
//                 let select_value = $(select).val(),
//                     first_select_value = $(select).find('option:first').val(),
//                     is_absent = select_value !== first_select_value
//                 if (is_absent)
//                     block_field_select(blocking_field)
//                 select.change((event) => {
//                     if (event.target.value === first_select_value) {
//                         unblock_field_select(blocking_field)
//                         select_first_option(id_condition_of_if_operator)
//                     } else
//                         block_field_select(blocking_field)
//                     block_or_unblock_field_multiple_select($operator_nesting)
//                 })
//             }
//
//             function select_first_option(select) {
//                 select.find('option:nth-child(2)').attr('selected', '')
//             }
//
//             function block_field_select(blocking_field) {
//                 let selected_value = $(blocking_field).val(),
//                     selected_value_blog = $(blocking_field).find('option[value="' + selected_value + '"]')
//                 selected_value_blog.val('')
//                 blocking_field.attr('disabled', true)
//             }
//
//             function unblock_field_select(blocking_field) {
//                 let selected_value = $(blocking_field).val(),
//                     selected_value_blog = $(blocking_field)
//                         .find('option[value="' + selected_value + '"]:not([style])'),
//                     selected_text_blog = selected_value_blog.text()
//                 selected_value_blog.val(selected_text_blog)
//                 blocking_field.removeAttr('disabled')
//             }
//
//
//             function block_or_unblock_field_multiple_select(multiple_select) {
//                 blocking_fields.forEach((blocking_field) => {
//                     if (is_options_selected(multiple_select[0]))
//                         unblock_field_select(blocking_field)
//                     else
//                         block_field_select(blocking_field)
//                 })
//             }
//
//             function is_options_selected(multiple_select) {
//                 let result = [],
//                     options = multiple_select && multiple_select.options,
//                     opt
//                 for (let i = 0, iLen = options.length; i < iLen; i++) {
//                     opt = options[i]
//                     if (opt.selected)
//                         result.push(opt.value || opt.text)
//                 }
//                 return result.length > 0
//             }
//
//             function block_or_unlock_operator_nesting() {
//                 $presence_one_of_cycles.change(()=>{
//
//                 })
//             }
//         }
//     }
// );
