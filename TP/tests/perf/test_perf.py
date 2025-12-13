"""Tests de performance pour le Triangulator."""

import time

import pytest

from src.triangulator.core import triangulate
from src.triangulator.serialization import deserialize_point_set, serialize_point_set


@pytest.mark.perf
def test_triangulation_performance_1000():
    """Test de performance de la triangulation avec 1000 points."""
    points = [(float(i % 100), float(i // 100)) for i in range(1000)]

    start_time = time.time()
    triangulate(points)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Triangulation de 1000 points: {duration:.4f} secondes")
    assert duration < 60


@pytest.mark.perf
def test_triangulation_performance_100():
    """Test de performance de la triangulation avec 100 points."""
    points = [(float(i % 10), float(i // 10)) for i in range(100)]

    start_time = time.time()
    triangulate(points)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Triangulation de 100 points: {duration:.4f} secondes")
    assert duration < 5


@pytest.mark.perf
def test_serialization_performance():
    """Test de performance de la sérialisation/désérialisation."""
    points = [(float(i), float(i)) for i in range(10000)]

    start_time = time.time()
    data = serialize_point_set(points)
    deserialize_point_set(data)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Sérialisation/Désérialisation de 10000 points: {duration:.4f} secondes")
    assert duration < 1
