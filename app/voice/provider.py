from abc import ABC,abstractmethod
class SpeechToTextProvider(ABC):
 @abstractmethod
 def transcribe(self,audio:bytes,filename:str): raise NotImplementedError
class TextToSpeechProvider(ABC):
 @abstractmethod
 def synthesize(self,text:str,voice:str,speed:float): raise NotImplementedError
