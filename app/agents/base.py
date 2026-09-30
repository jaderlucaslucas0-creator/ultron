from dataclasses import dataclass
from typing import Callable

@dataclass
class Agent:
    name: str
    description: str
    instructions: str
    handler: Callable | None = None

    def run(self,text:str,context:str="")->str:
        if self.handler:
            return self.handler(text,context)
        return f"Agente {self.name} pronto para processar a solicitação."
