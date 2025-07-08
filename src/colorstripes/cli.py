"""
Command-line interface for ColorStripes.
"""

from typing import Optional, Literal

import click
import matplotlib.pyplot as plt

from .generator import ColormapGenerator
from .utils import save_colormap


@click.command()
@click.option(
    '--name', '-n',
    default='custom',
    help='Name for the colormap'
)
@click.option(
    '--seed', '-s',
    type=int,
    help='Random seed for reproducibility'
)
@click.option(
    '--output', '-o',
    help='Output file path (without extension)'
)
@click.option(
    '--format', '-f',
    type=click.Choice(['png', 'json', 'both']),
    default='both',
    help='Output format'
)
@click.option(
    '--n-points',
    type=int,
    default=256,
    help='Number of points in colormap'
)
@click.option(
    '--stripe-frequency',
    type=float,
    help='Base frequency of stripes'
)
@click.option(
    '--show/--no-show',
    default=True,
    help='Display the generated colormap'
)
def main(
    name: str,
    seed: Optional[int],
    output: Optional[str],
    format: Literal["png", "json", "both"],
    n_points: int,
    stripe_frequency: Optional[float],
    show: bool
) -> None:
    """Generate randomized colormaps with smooth transitions and stripe patterns."""
    
    generator = ColormapGenerator(n_points=n_points, seed=seed)
    
    # Prepare parameters
    params = {}
    if stripe_frequency is not None:
        params['stripe_frequency'] = stripe_frequency
    
    # Generate colormap
    cmap = generator.generate_colormap(name, **params)
    
    # Create and display swatch
    swatch = generator.create_swatch(cmap, width=800, height=60)
    
    if show:
        plt.figure(figsize=(10, 2))
        plt.imshow(swatch, aspect='auto')
        plt.title(name, loc='left', fontsize=16)
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    
    # Save colormap
    if output:
        save_colormap(cmap, output, format)
        
        # Save swatch image
        if format in ['png', 'both']:
            plt.figure(figsize=(10, 2))
            plt.imshow(swatch, aspect='auto')
            plt.title(name, loc='left', fontsize=16)
            plt.axis('off')
            plt.tight_layout()
            plt.savefig(f"{output}_swatch.png", dpi=150, bbox_inches='tight')
            click.echo(f"Saved swatch to {output}_swatch.png")


if __name__ == '__main__':
    main()