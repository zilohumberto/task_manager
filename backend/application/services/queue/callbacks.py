

def finished_callback(task_listener, repository, **kwargs):
    repository.mark_done(pk=task_listener.get_name())
