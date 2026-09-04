from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class Chunk:id:str;text:str;source:str;page:int;module:str
@dataclass(frozen=True,slots=True)
class Hit:chunk:Chunk;score:float
