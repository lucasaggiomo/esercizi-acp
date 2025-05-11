from abc import ABC, abstractmethod

class DispatcherService(ABC):
	@abstractmethod
	def sendCommand(self, command):
		pass

	@abstractmethod
	def getCommand(self):
		pass
