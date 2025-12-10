"""Tests unitaires pour le module core de triangulation."""

from src.triangulator.core import triangulate


def test_triangulate_simple_triangle():
    """Test de triangulation de 3 points formant un triangle."""
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    triangles = triangulate(points)
    assert len(triangles) == 1
    t = triangles[0]
    assert set(t) == {0, 1, 2}


def test_triangulate_square():
    """Test de triangulation de 4 points formant un carré."""
    points = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    triangles = triangulate(points)
    assert len(triangles) == 2


def test_triangulate_less_than_3_points():
    """Test avec moins de 3 points: aucun triangle possible."""
    points = [(0.0, 0.0), (1.0, 1.0)]
    triangles = triangulate(points)
    assert len(triangles) == 0


def test_triangulate_collinear_points():
    """Test avec des points colinéaires: aucun triangle possible."""
    points = [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)]
    triangles = triangulate(points)
    assert len(triangles) == 0


def test_triangulate_coincident_points():
    """Test avec des points coïncidents: aucun triangle possible."""
    points = [(0.0, 0.0), (0.0, 0.0), (1.0, 1.0)]
    triangles = triangulate(points)
    assert len(triangles) == 0


def test_triangulate_empty():
    """Test avec un ensemble vide de points."""
    points = []
    triangles = triangulate(points)
    assert len(triangles) == 0


def test_triangulate_large_set():
    """Test avec un ensemble plus grand de points."""
    points = [(float(i), float(i * 2)) for i in range(10)]
    triangles = triangulate(points)
    assert isinstance(triangles, list)
