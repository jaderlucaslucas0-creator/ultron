from dataclasses import dataclass,field
from typing import Any,Callable

@dataclass
class Plugin:
    name:str
    description:str
    capabilities:list[str]=field(default_factory=list)
    enabled:bool=True
    handler:Callable|None=None

PLUGINS:dict[str,Plugin]={}

def register_plugin(plugin:Plugin):
    PLUGINS[plugin.name]=plugin

def list_plugins():
    return [{'name':p.name,'description':p.description,'capabilities':p.capabilities,'enabled':p.enabled} for p in PLUGINS.values()]

def get_plugin(name:str): return PLUGINS.get(name)

def execute_plugin(name:str,payload:dict[str,Any]):
    plugin=get_plugin(name)
    if not plugin: raise KeyError('Plugin não encontrado.')
    if not plugin.enabled: raise RuntimeError('Plugin desativado.')
    if not plugin.handler: raise RuntimeError('Plugin sem executor.')
    return plugin.handler(payload)
