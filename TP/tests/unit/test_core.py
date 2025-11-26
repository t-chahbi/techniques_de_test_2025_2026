import pytest
from src.triangulator.core import triangulate

def test_triangulate_simple_triangle():
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    # Should return one triangle connecting these 3 points
    triangles = triangulate(points)
    assert len(triangles) == 1
    # Check that the triangle uses indices 0, 1, 2
    t = triangles[0]
    assert set(t) == {0, 1, 2}

def test_triangulate_square():
    points = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    triangles = triangulate(points)
    # A square should be split into 2 triangles
    assert len(triangles) == 2

def test_triangulate_less_than_3_points():
    points = [(0.0, 0.0), (1.0, 1.0)]
    triangles = triangulate(points)
    assert len(triangles) == 0

def test_triangulate_collinear_points():
    points = [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)]
    triangles = triangulate(points)
    assert len(triangles) == 0

def test_triangulate_coincident_points():
    points = [(0.0, 0.0), (0.0, 0.0), (1.0, 1.0)]
    triangles = triangulate(points)
    assert len(triangles) == 0
