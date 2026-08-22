# IMPORTS
import importlib

def verificar_instalacion(libreria):
    """Check whether a library is installed."""
    spec = importlib.util.find_spec(libreria)
    return spec is not None
