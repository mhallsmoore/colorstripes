"""
Tests for the command-line interface.
"""

import pytest
from click.testing import CliRunner
from pathlib import Path
import json

from colorstripes.cli import main


class TestCLI:
    """Test the command-line interface."""
    
    @pytest.fixture
    def runner(self):
        """Create a CLI runner."""
        return CliRunner()
    
    def test_basic_generation(self, runner):
        """Test basic colormap generation."""
        result = runner.invoke(main, ['--no-show'])
        assert result.exit_code == 0
    
    def test_with_name(self, runner):
        """Test generation with custom name."""
        result = runner.invoke(main, ['--name', 'my_colormap', '--no-show'])
        assert result.exit_code == 0
    
    def test_with_seed(self, runner):
        """Test generation with seed for reproducibility."""
        # Generate twice with same seed
        result1 = runner.invoke(main, ['--seed', '42', '--no-show'])
        result2 = runner.invoke(main, ['--seed', '42', '--no-show'])
        
        assert result1.exit_code == 0
        assert result2.exit_code == 0
    
    def test_save_json(self, runner, tmp_path):
        """Test saving as JSON."""
        output_path = tmp_path / "test_output"
        
        result = runner.invoke(main, [
            '--output', str(output_path),
            '--format', 'json',
            '--no-show'
        ])
        
        assert result.exit_code == 0
        assert output_path.with_suffix('.json').exists()
        
        # Verify JSON content
        with open(output_path.with_suffix('.json'), 'r') as f:
            data = json.load(f)
        
        assert 'colors' in data
        assert data['n_colors'] == 256
    
    def test_save_png(self, runner, tmp_path):
        """Test saving as PNG."""
        output_path = tmp_path / "test_output"
        
        result = runner.invoke(main, [
            '--output', str(output_path),
            '--format', 'png',
            '--no-show'
        ])
        
        assert result.exit_code == 0
        assert output_path.with_suffix('.png').exists()
        assert (output_path.parent / f"{output_path.name}_swatch.png").exists()
    
    def test_save_both(self, runner, tmp_path):
        """Test saving in both formats."""
        output_path = tmp_path / "test_output"
        
        result = runner.invoke(main, [
            '--output', str(output_path),
            '--format', 'both',
            '--no-show'
        ])
        
        assert result.exit_code == 0
        assert output_path.with_suffix('.json').exists()
        assert output_path.with_suffix('.png').exists()
        assert (output_path.parent / f"{output_path.name}_swatch.png").exists()
    
    def test_custom_n_points(self, runner):
        """Test generation with custom number of points."""
        result = runner.invoke(main, [
            '--n-points', '512',
            '--no-show'
        ])
        
        assert result.exit_code == 0
    
    def test_stripe_frequency(self, runner):
        """Test custom stripe frequency."""
        result = runner.invoke(main, [
            '--stripe-frequency', '80',
            '--no-show'
        ])
        
        assert result.exit_code == 0
    
    def test_all_options(self, runner, tmp_path):
        """Test with all options combined."""
        output_path = tmp_path / "full_test"
        
        result = runner.invoke(main, [
            '--name', 'full_test',
            '--seed', '123',
            '--output', str(output_path),
            '--format', 'both',
            '--n-points', '128',
            '--stripe-frequency', '60',
            '--no-show'
        ])
        
        assert result.exit_code == 0
        assert output_path.with_suffix('.json').exists()
        assert output_path.with_suffix('.png').exists()
        
        # Verify JSON has correct number of points
        with open(output_path.with_suffix('.json'), 'r') as f:
            data = json.load(f)
        assert data['n_colors'] == 256  # Always saves 256 colors
        assert data['name'] == 'full_test'
    
    def test_help(self, runner):
        """Test help message."""
        result = runner.invoke(main, ['--help'])
        assert result.exit_code == 0
        assert 'Generate randomized colormaps' in result.output
        assert '--name' in result.output
        assert '--seed' in result.output
        assert '--stripe-frequency' in result.output
    
    def test_invalid_format(self, runner):
        """Test invalid format option."""
        result = runner.invoke(main, ['--format', 'invalid'])
        assert result.exit_code != 0
        assert 'Invalid value' in result.output