"""
Core colormap generation functionality.
"""

import numpy as np
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
from typing import Tuple, Optional, Dict, Any


class ColormapGenerator:
    """Generate complex colormaps with background transitions and stripe patterns."""
    
    def __init__(self, n_points: int = 256, seed: Optional[int] = None) -> None:
        """
        Initialize the colormap generator.
        
        Parameters:
        -----------
        n_points : int
            Number of points in the colormap
        seed : int or None
            Random seed for reproducibility
        """
        self.n_points = n_points
        if seed is not None:
            np.random.seed(seed)
    
    def generate_smooth_base(
        self,
        n_control_points: int = 5,
        hue_range: Tuple[float, float] = (0, 1),
        saturation_range: Tuple[float, float] = (0.3, 0.9),
        value_range: Tuple[float, float] = (0.4, 0.95)
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Generate smooth background color transitions using spline interpolation.
        
        Parameters:
        -----------
        n_control_points : int
            Number of control points for the smooth transition
        hue_range : tuple
            Range of hues (0-1) to use
        saturation_range : tuple
            Range of saturation values
        value_range : tuple
            Range of value/brightness values
            
        Returns:
        --------
        tuple
            Arrays of hue, saturation, and value components
        """
        # Generate control points
        x_control = np.linspace(0, 1, n_control_points)
        
        # Generate smooth transitions for HSV components
        hue_control = np.random.uniform(*hue_range, n_control_points)
        sat_control = np.random.uniform(*saturation_range, n_control_points)
        val_control = np.random.uniform(*value_range, n_control_points)
        
        # Add some structure to hue transitions
        hue_control = np.cumsum(np.random.uniform(-0.3, 0.3, n_control_points))
        hue_control = (hue_control - hue_control.min()) / (hue_control.max() - hue_control.min() + 1e-8)
        hue_control = hue_control * (hue_range[1] - hue_range[0]) + hue_range[0]
        
        # Interpolate to full resolution
        x = np.linspace(0, 1, self.n_points)
        hue = np.interp(x, x_control, hue_control)
        sat = np.interp(x, x_control, sat_control)
        val = np.interp(x, x_control, val_control)
        
        # Add varying rate of change using sine waves
        freq = np.random.uniform(1, 4)
        phase = np.random.uniform(0, 2*np.pi)
        amplitude = np.random.uniform(0.05, 0.15)
        hue += amplitude * np.sin(freq * 2 * np.pi * x + phase)
        
        # Ensure hue wraps correctly
        # For restricted hue ranges, clip instead of wrap to maintain range
        if hue_range[1] - hue_range[0] < 0.8:  # If range is restricted
            hue = np.clip(hue, 0, 1)
        else:
            hue = hue % 1.0
        
        return hue, sat, val
    
    def generate_stripes(
        self,
        base_frequency: float = 50,
        frequency_variation: float = 0.5,
        amplitude_range: Tuple[float, float] = (0.05, 0.2)
    ) -> np.ndarray:
        """
        Generate stripe patterns with varying widths and intensities.
        
        Parameters:
        -----------
        base_frequency : float
            Base frequency of stripes
        frequency_variation : float
            How much the frequency varies (0-1)
        amplitude_range : tuple
            Range of stripe amplitudes
            
        Returns:
        --------
        np.ndarray
            Array of stripe values
        """
        x = np.linspace(0, 1, self.n_points)
        stripes = np.zeros_like(x)
        
        # Generate multiple stripe components
        n_components = np.random.randint(3, 7)
        
        for i in range(n_components):
            # Varying frequency
            freq = base_frequency * np.random.uniform(
                1 - frequency_variation, 
                1 + frequency_variation
            )
            
            # Varying phase
            phase = np.random.uniform(0, 2*np.pi)
            
            # Varying amplitude that changes across the colormap
            amp_start = np.random.uniform(*amplitude_range)
            amp_end = np.random.uniform(*amplitude_range)
            amplitude = np.linspace(amp_start, amp_end, self.n_points)
            
            # Add frequency modulation for varying stripe width
            freq_mod = 1 + 0.3 * np.sin(2 * np.pi * x * np.random.uniform(0.5, 2))
            
            # Generate stripe component
            stripe_component = amplitude * np.sin(2 * np.pi * freq * freq_mod * x + phase)
            
            # Randomly use different waveforms for variety
            if np.random.random() > 0.5:
                # Square-ish waves for sharper stripes
                stripe_component = amplitude * np.tanh(5 * stripe_component)
            
            stripes += stripe_component
        
        return stripes
    
    def hsv_to_rgb(
        self,
        h: np.ndarray,
        s: np.ndarray,
        v: np.ndarray
    ) -> np.ndarray:
        """
        Convert HSV arrays to RGB.
        
        Parameters:
        -----------
        h : np.ndarray
            Hue values (0-1)
        s : np.ndarray
            Saturation values (0-1)
        v : np.ndarray
            Value/brightness values (0-1)
            
        Returns:
        --------
        np.ndarray
            RGB values array of shape (n_points, 3)
        """
        # Stack HSV channels
        hsv = np.stack([h, s, v], axis=-1)
        
        # Convert to RGB
        rgb = np.zeros_like(hsv)
        for i in range(len(h)):
            rgb[i] = mcolors.hsv_to_rgb([hsv[i, 0], hsv[i, 1], hsv[i, 2]])
        
        return rgb
    
    def generate_colormap(
        self,
        name: str = "custom",
        **kwargs: Any
    ) -> LinearSegmentedColormap:
        """
        Generate a complete colormap.
        
        Parameters:
        -----------
        name : str
            Name for the colormap
        **kwargs : dict
            Additional parameters for generation:
            - n_control_points: int
            - hue_range: Tuple[float, float]
            - saturation_range: Tuple[float, float]
            - value_range: Tuple[float, float]
            - stripe_frequency: float
            - frequency_variation: float
            - hue_stripe_amplitude: Tuple[float, float]
            - val_stripe_amplitude: Tuple[float, float]
        
        Returns:
        --------
        LinearSegmentedColormap
            The generated colormap
        """
        # Generate base colors
        hue, sat, val = self.generate_smooth_base(
            n_control_points=kwargs.get('n_control_points', 5),
            hue_range=kwargs.get('hue_range', (0, 1)),
            saturation_range=kwargs.get('saturation_range', (0.3, 0.9)),
            value_range=kwargs.get('value_range', (0.4, 0.95))
        )
        
        # Generate stripes
        hue_stripes = self.generate_stripes(
            base_frequency=kwargs.get('stripe_frequency', 50),
            frequency_variation=kwargs.get('frequency_variation', 0.5),
            amplitude_range=kwargs.get('hue_stripe_amplitude', (0.02, 0.08))
        )
        
        val_stripes = self.generate_stripes(
            base_frequency=kwargs.get('stripe_frequency', 50) * 1.5,
            frequency_variation=kwargs.get('frequency_variation', 0.3),
            amplitude_range=kwargs.get('val_stripe_amplitude', (0.05, 0.15))
        )
        
        # Apply stripes
        hue = (hue + hue_stripes) % 1.0
        val = np.clip(val + val_stripes, 0, 1)
        
        # Add subtle saturation variation
        sat_variation = 0.05 * np.sin(20 * np.pi * np.linspace(0, 1, self.n_points))
        sat = np.clip(sat + sat_variation, 0, 1)
        
        # Convert to RGB
        rgb = self.hsv_to_rgb(hue, sat, val)
        
        # Create colormap
        cmap = LinearSegmentedColormap.from_list(name, rgb, N=self.n_points)
        
        return cmap
    
    def create_swatch(
        self,
        cmap: LinearSegmentedColormap,
        width: int = 800,
        height: int = 60
    ) -> np.ndarray:
        """
        Create a swatch image of the colormap.
        
        Parameters:
        -----------
        cmap : matplotlib colormap
            The colormap to visualize
        width : int
            Width of the swatch in pixels
        height : int
            Height of the swatch in pixels
        
        Returns:
        --------
        numpy.ndarray
            The swatch image of shape (height, width, 4)
        """
        gradient = np.linspace(0, 1, width).reshape(1, -1)
        gradient = np.repeat(gradient, height, axis=0)
        
        return cmap(gradient)