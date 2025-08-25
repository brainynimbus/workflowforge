"""Definición de triggers para workflows de GitHub Actions."""

from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field
from abc import ABC, abstractmethod


class Trigger(BaseModel, ABC):
    """Clase base abstracta para triggers."""
    
    @abstractmethod
    def to_dict(self) -> Union[str, Dict[str, Any]]:
        """Convierte el trigger a formato para YAML."""
        pass


class PushTrigger(Trigger):
    """Trigger para eventos push."""
    
    branches: Optional[List[str]] = Field(None, description="Ramas que disparan el trigger")
    branches_ignore: Optional[List[str]] = Field(None, description="Ramas a ignorar")
    tags: Optional[List[str]] = Field(None, description="Tags que disparan el trigger")
    tags_ignore: Optional[List[str]] = Field(None, description="Tags a ignorar")
    paths: Optional[List[str]] = Field(None, description="Rutas que disparan el trigger")
    paths_ignore: Optional[List[str]] = Field(None, description="Rutas a ignorar")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario."""
        result = {}
        if self.branches:
            result["branches"] = self.branches
        if self.branches_ignore:
            result["branches-ignore"] = self.branches_ignore
        if self.tags:
            result["tags"] = self.tags
        if self.tags_ignore:
            result["tags-ignore"] = self.tags_ignore
        if self.paths:
            result["paths"] = self.paths
        if self.paths_ignore:
            result["paths-ignore"] = self.paths_ignore
        
        return {"push": result} if result else "push"


class PullRequestTrigger(Trigger):
    """Trigger para eventos pull request."""
    
    types: Optional[List[str]] = Field(None, description="Tipos de eventos PR")
    branches: Optional[List[str]] = Field(None, description="Ramas objetivo")
    branches_ignore: Optional[List[str]] = Field(None, description="Ramas a ignorar")
    paths: Optional[List[str]] = Field(None, description="Rutas que disparan el trigger")
    paths_ignore: Optional[List[str]] = Field(None, description="Rutas a ignorar")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario."""
        result = {}
        if self.types:
            result["types"] = self.types
        if self.branches:
            result["branches"] = self.branches
        if self.branches_ignore:
            result["branches-ignore"] = self.branches_ignore
        if self.paths:
            result["paths"] = self.paths
        if self.paths_ignore:
            result["paths-ignore"] = self.paths_ignore
        
        return {"pull_request": result} if result else "pull_request"


class ScheduleTrigger(Trigger):
    """Trigger para eventos programados (cron)."""
    
    cron: str = Field(..., description="Expresión cron")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario."""
        return {"schedule": [{"cron": self.cron}]}


class WorkflowDispatchTrigger(Trigger):
    """Trigger para ejecución manual."""
    
    inputs: Optional[Dict[str, Dict[str, Any]]] = Field(None, description="Inputs del workflow")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario."""
        result = {}
        if self.inputs:
            result["inputs"] = self.inputs
        return {"workflow_dispatch": result} if result else "workflow_dispatch"


class ReleaseTrigger(Trigger):
    """Trigger para eventos de release."""
    
    types: Optional[List[str]] = Field(None, description="Tipos de eventos de release")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario."""
        result = {}
        if self.types:
            result["types"] = self.types
        return {"release": result} if result else "release"


# Factory functions para crear triggers fácilmente
def on_push(branches: Optional[List[str]] = None, paths: Optional[List[str]] = None) -> PushTrigger:
    """Crea un PushTrigger de manera conveniente."""
    return PushTrigger(branches=branches, paths=paths)


def on_pull_request(branches: Optional[List[str]] = None, types: Optional[List[str]] = None) -> PullRequestTrigger:
    """Crea un PullRequestTrigger de manera conveniente."""
    return PullRequestTrigger(branches=branches, types=types)


def on_schedule(cron: str) -> ScheduleTrigger:
    """Crea un ScheduleTrigger de manera conveniente."""
    return ScheduleTrigger(cron=cron)


def on_workflow_dispatch(inputs: Optional[Dict[str, Dict[str, Any]]] = None) -> WorkflowDispatchTrigger:
    """Crea un WorkflowDispatchTrigger de manera conveniente."""
    return WorkflowDispatchTrigger(inputs=inputs)


def on_release(types: Optional[List[str]] = None) -> ReleaseTrigger:
    """Crea un ReleaseTrigger de manera conveniente."""
    return ReleaseTrigger(types=types)