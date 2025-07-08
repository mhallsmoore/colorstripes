"""
Pytest configuration and shared fixtures.
"""

import matplotlib
import matplotlib.pyplot as plt
import pytest


@pytest.fixture(autouse=True)
def configure_matplotlib():
    """Configure matplotlib for testing."""
    # Use non-interactive backend for tests
    matplotlib.use('Agg')
    
    # Close all figures after each test to prevent memory issues
    yield
    plt.close('all')


@pytest.fixture
def no_random_seed():
    """Fixture to ensure tests don't affect each other's randomness."""
    import numpy as np
    # Save current random state
    state = np.random.get_state()
    yield
    # Restore random state
    np.random.set_state(state)