"""Definición de entornos para jobs."""

from typing import Dict, Optional, Any
from pydantic import BaseModel, Field


class Environment(BaseModel):
    """Representa un entorno de despliegue."""
    
    name: str = Field(..., description="Nombre del entorno")
    url: Optional[str] = Field(None, description="URL del entorno")
    
    def model_dump(self, **kwargs) -> Dict[str, Any]:
        """Serializa el entorno."""
        result = {"name": self.name}
        if self.url:
            result["url"] = self.url
        return result


# Factory function para crear entornos fácilmente
def environment(name: str, url: Optional[str] = None) -> Environment:
    """Crea un Environment de manera conveniente."""
    return Environment(name=name, url=url)