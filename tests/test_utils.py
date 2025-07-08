"""
Tests for utility functions.
"""

import json
from pathlib import Path
import tempfile

from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pytest

from colorstripes import ColormapGenerator
from colorstripes.utils import save_colormap, load_colormap_from_json


class TestUtils:
    """Test utility functions."""
    
    @pytest.fixture
    def sample_colormap(self):
        """Create a sample colormap for testing."""
        gen = ColormapGenerator(seed=42)
        return gen.generate_colormap(name="test_colormap")
    
    def test_save_colormap_json(self, sample_colormap, tmp_path):
        """Test saving colormap as JSON."""
        output_path = tmp_path / "test_cmap"
        
        save_colormap(sample_colormap, str(output_path), format="json")
        
        json_file = output_path.with_suffix(".json")
        assert json_file.exists()
        
        # Load and verify JSON content
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        assert data["name"] == "test_colormap"
        assert "colors" in data
        assert len(data["colors"]) == 256
        assert data["n_colors"] == 256
        
        # Verify color format
        assert all(len(color) == 3 for color in data["colors"])
        assert all(
            all(0 <= c <= 1 for c in color)
            for color in data["colors"]
        )
    
    def test_save_colormap_png(self, sample_colormap, tmp_path):
        """Test saving colormap as PNG."""
        output_path = tmp_path / "test_cmap"
        
        save_colormap(sample_colormap, str(output_path), format="png")
        
        png_file = output_path.with_suffix(".png")
        assert png_file.exists()
        
        # Check file is not empty
        assert png_file.stat().st_size > 0
    
    def test_save_colormap_both(self, sample_colormap, tmp_path):
        """Test saving colormap in both formats."""
        output_path = tmp_path / "test_cmap"
        
        save_colormap(sample_colormap, str(output_path), format="both")
        
        json_file = output_path.with_suffix(".json")
        png_file = output_path.with_suffix(".png")
        
        assert json_file.exists()
        assert png_file.exists()
    
    def test_load_colormap_from_json(self, sample_colormap, tmp_path):
        """Test loading colormap from JSON."""
        # First save a colormap
        output_path = tmp_path / "test_cmap"
        save_colormap(sample_colormap, str(output_path), format="json")
        
        # Load it back
        json_file = output_path.with_suffix(".json")
        loaded_cmap = load_colormap_from_json(str(json_file))
        
        assert isinstance(loaded_cmap, LinearSegmentedColormap)
        assert loaded_cmap.name == "test_colormap"
        
        # Compare colors (should be very close but may have small numerical differences)
        original_colors = sample_colormap(np.linspace(0, 1, 10))
        loaded_colors = loaded_cmap(np.linspace(0, 1, 10))
        
        np.testing.assert_array_almost_equal(
            original_colors[:, :3],  # Ignore alpha
            loaded_colors[:, :3],
            decimal=3
        )
    
    def test_round_trip_consistency(self, tmp_path):
        """Test that saving and loading preserves colormap data."""
        # Generate colormap
        gen = ColormapGenerator(seed=123)
        original_cmap = gen.generate_colormap(name="round_trip_test")
        
        # Save and load
        output_path = tmp_path / "round_trip"
        save_colormap(original_cmap, str(output_path), format="json")
        loaded_cmap = load_colormap_from_json(str(output_path.with_suffix(".json")))
        
        # Compare at multiple points
        test_points = np.linspace(0, 1, 50)
        original_colors = original_cmap(test_points)[:, :3]
        loaded_colors = loaded_cmap(test_points)[:, :3]
        
        np.testing.assert_array_almost_equal(
            original_colors,
            loaded_colors,
            decimal=5
        )
    
    def test_invalid_format(self, sample_colormap, tmp_path):
        """Test handling of invalid format."""
        output_path = tmp_path / "test_cmap"
        
        # This should work without error (type checking would catch this in real usage)
        # but we test the logic handles it gracefully
        save_colormap(sample_colormap, str(output_path), format="invalid")  # type: ignore
        
        # No files should be created for invalid format
        assert not output_path.with_suffix(".json").exists()
        assert not output_path.with_suffix(".png").exists()
    
    def test_load_invalid_json(self, tmp_path):
        """Test loading from invalid JSON file."""
        # Create invalid JSON
        json_file = tmp_path / "invalid.json"
        json_file.write_text("not valid json")
        
        with pytest.raises(json.JSONDecodeError):
            load_colormap_from_json(str(json_file))
    
    def test_load_missing_fields(self, tmp_path):
        """Test loading JSON with missing fields."""
        # Create JSON with missing colors
        json_file = tmp_path / "incomplete.json"
        with open(json_file, 'w') as f:
            json.dump({"name": "incomplete"}, f)
        
        with pytest.raises(KeyError):
            load_colormap_from_json(str(json_file))