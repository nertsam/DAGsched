from abc import ABC, abstractmethod


class SchedulingTest(ABC):
	def __init__(self, model):
		super(SchedulingTest, self).__init__()

	@abstractmethod
	def schedulable(self, taskset):
		pass

