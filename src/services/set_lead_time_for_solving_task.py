def set_lead_time_for_solving_task(testing, solving_task):
    is_set_time = not testing.lead_time
    if is_set_time:
        solving_task.time_left = testing.task_lead_time if testing.task_lead_time else solving_task.task.lead_time
        solving_task.save()
