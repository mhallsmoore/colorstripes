import matplotlib.pyplot as plt

from colorstripes import ColormapGenerator


if __name__ == "__main__":
    generator = ColormapGenerator()

    # Generate multiple colormaps
    fig, axes = plt.subplots(5, 1, figsize=(10, 6))

    for idx in range(5):
        cmap = generator.generate_colormap(name=f"colormap_{idx}")
        swatch = generator.create_swatch(cmap)
        axes[idx].imshow(swatch, aspect='auto')
        axes[idx].axis('off')
        axes[idx].set_title(f"Colormap {idx}", loc='left')

    plt.tight_layout()
    plt.show()