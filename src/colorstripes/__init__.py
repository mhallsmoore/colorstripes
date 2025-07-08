"""
ColorStripes - Generate randomized colormaps with
smooth transitions and stripe patterns.
"""

from .generator import ColormapGenerator
from .utils import save_colormap

__version__ = "0.1.0"
__all__ = ["ColormapGenerator", "save_colormap"]