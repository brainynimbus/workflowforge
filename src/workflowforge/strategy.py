"""Definición de estrategias y matrices para jobs."""

from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field


class Matrix(BaseModel):
    """Representa una matriz de build."""
    
    model_config = {"extra": "allow"}
    
    include: Optional[List[Dict[str, Any]]] = Field(None, description="Configuraciones adicionales")
    exclude: Optional[List[Dict[str, Any]]] = Field(None, description="Configuraciones a excluir")
    

    
    def model_dump(self, **kwargs) -> Dict[str, Any]:
        """Serializa la matriz incluyendo variables dinámicas."""
        result = super().model_dump(**kwargs)
        return {k: v for k, v in result.items() if v is not None}


class Strategy(BaseModel):
    """Representa una estrategia de ejecución para jobs."""
    
    matrix: Optional[Matrix] = Field(None, description="Matriz de configuraciones")
    fail_fast: Optional[bool] = Field(None, description="Fallar rápido si hay error")
    max_parallel: Optional[int] = Field(None, description="Máximo de jobs paralelos")
    
    def model_dump(self, **kwargs) -> Dict[str, Any]:
        """Serializa la estrategia."""
        result = {}
        
        if self.matrix:
            result["matrix"] = self.matrix.model_dump(**kwargs)
        if self.fail_fast is not None:
            result["fail-fast"] = self.fail_fast
        if self.max_parallel is not None:
            result["max-parallel"] = self.max_parallel
        
        return result


# Factory functions para crear estrategias fácilmente
def matrix(**variables) -> Matrix:
    """Crea una Matrix de manera conveniente."""
    return Matrix(**variables)


def strategy(matrix: Optional[Matrix] = None, fail_fast: Optional[bool] = None, max_parallel: Optional[int] = None) -> Strategy:
    """Crea una Strategy de manera conveniente."""
    return Strategy(matrix=matrix, fail_fast=fail_fast, max_parallel=max_parallel)