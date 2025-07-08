import matplotlib.pyplot as plt

from colorstripes import ColormapGenerator


if __name__ == "__main__":
    generator = ColormapGenerator()

    # Generate with specific color characteristics
    cmap = generator.generate_colormap(
        name="ocean_waves",
        hue_range=(0.5, 0.6),        # Blue-cyan range
        saturation_range=(0.3, 0.8),  # Varied saturation
        value_range=(0.3, 0.9),       # Dark to light
        n_control_points=7,           # More control points for complexity
        stripe_frequency=45,          # Wider stripes
        frequency_variation=0.7,      # More variation in stripe width
        hue_stripe_amplitude=(0.01, 0.04),  # Subtle hue variations
        val_stripe_amplitude=(0.1, 0.25)    # Stronger brightness stripes
    )

    # Generate colormap swatch
    fig, ax = plt.subplots(1, 1, figsize=(10, 1.5))

    swatch = generator.create_swatch(cmap)
    ax.imshow(swatch, aspect='auto')
    ax.axis('off')
    ax.set_title(f"Colormap 'Ocean Waves'", loc='left')

    plt.tight_layout()
    plt.show()