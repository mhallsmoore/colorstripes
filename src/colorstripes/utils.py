"""
Utility functions for colormap handling and export.
"""

import json
from typing import Literal, Union

from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import numpy as np


def save_colormap(
    cmap: LinearSegmentedColormap,
    output_path: str,
    format: Union[Literal["json"], Literal["png"], Literal["both"]] = "both"
) -> None:
    """
    Save colormap in specified format(s).
    
    Parameters:
    -----------
    cmap : LinearSegmentedColormap
        The colormap to save
    output_path : str
        Base output path (without extension)
    format : str
        Output format: 'json', 'png', or 'both'
    """
    if format in ["json", "both"]:
        # Save as JSON (RGB values)
        colors = cmap(np.linspace(0, 1, 256))[:, :3]  # Remove alpha channel
        cmap_data = {
            "name": cmap.name,
            "colors": colors.tolist(),
            "n_colors": len(colors)
        }
        
        json_path = f"{output_path}.json"
        with open(json_path, "w") as f:
            json.dump(cmap_data, f, indent=2)
        print(f"Saved colormap data to {json_path}")
    
    if format in ["png", "both"]:
        # Save as gradient image
        gradient = np.linspace(0, 1, 1000).reshape(1, -1)
        gradient = np.repeat(gradient, 100, axis=0)
        
        plt.figure(figsize=(10, 1))
        plt.imshow(gradient, cmap=cmap, aspect='auto')
        plt.axis('off')
        plt.tight_layout()
        
        png_path = f"{output_path}.png"
        plt.savefig(png_path, dpi=150, bbox_inches='tight', pad_inches=0)
        plt.close()
        print(f"Saved colormap gradient to {png_path}")


def load_colormap_from_json(json_path: str) -> LinearSegmentedColormap:
    """
    Load a colormap from a JSON file.
    
    Parameters:
    -----------
    json_path : str
        Path to the JSON file
        
    Returns:
    --------
    LinearSegmentedColormap
        The loaded colormap
    """
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    colors = np.array(data['colors'])
    name = data.get('name', 'custom')
    
    return LinearSegmentedColormap.from_list(name, colors)