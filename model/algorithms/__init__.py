
def required_model(name: object, kwargs: object) -> object:
	required_fields = kwargs['required_fields'] if 'required_fields' in kwargs else []
	task_f = kwargs['required_task_fields'] if 'required_task_fields' in kwargs else []
	proc_f = kwargs['required_proc_fields'] if 'required_proc_fields' in kwargs else []
	display_name = kwargs['display_name'] if 'display_name' in kwargs else name

	def f(klass):
		return klass
	return f