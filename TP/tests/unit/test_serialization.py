"""Tests unitaires pour le module de sérialisation."""

import struct

import pytest

from src.triangulator.serialization import (
    deserialize_point_set,
    serialize_point_set,
    serialize_triangles,
)


def test_serialize_point_set_nominal():
    """Test de sérialisation d'un PointSet nominal."""
    points = [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)]
    expected = struct.pack('<I', 3) + \
               struct.pack('<ff', 0.0, 0.0) + \
               struct.pack('<ff', 1.0, 1.0) + \
               struct.pack('<ff', 2.0, 2.0)

    assert serialize_point_set(points) == expected


def test_deserialize_point_set_nominal():
    """Test de désérialisation d'un PointSet nominal."""
    data = struct.pack('<I', 3) + \
           struct.pack('<ff', 0.0, 0.0) + \
           struct.pack('<ff', 1.0, 1.0) + \
           struct.pack('<ff', 2.0, 2.0)

    expected = [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)]
    assert deserialize_point_set(data) == expected


def test_serialize_deserialize_round_trip():
    """Test de round-trip sérialisation/désérialisation."""
    points = [(1.5, 2.5), (-1.0, 0.0)]
    serialized = serialize_point_set(points)
    deserialized = deserialize_point_set(serialized)
    assert deserialized == points


def test_serialize_empty_point_set():
    """Test de sérialisation d'un PointSet vide."""
    points = []
    expected = struct.pack('<I', 0)
    assert serialize_point_set(points) == expected
    assert deserialize_point_set(expected) == points


def test_deserialize_malformed_data_length():
    """Test de désérialisation avec données malformées."""
    data = struct.pack('<I', 1)
    with pytest.raises(ValueError):
        deserialize_point_set(data)


def test_serialize_triangles_nominal():
    """Test de sérialisation de Triangles nominal."""
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    triangles = [(0, 1, 2)]

    expected = struct.pack('<I', 3) + \
               struct.pack('<ff', 0.0, 0.0) + \
               struct.pack('<ff', 1.0, 0.0) + \
               struct.pack('<ff', 0.0, 1.0)

    expected += struct.pack('<I', 1) + \
                struct.pack('<III', 0, 1, 2)

    assert serialize_triangles(points, triangles) == expected


def test_serialize_triangles_empty():
    """Test de sérialisation de triangles vides."""
    points = [(0.0, 0.0), (1.0, 0.0)]
    triangles = []

    result = serialize_triangles(points, triangles)
    expected = struct.pack('<I', 2) + \
               struct.pack('<ff', 0.0, 0.0) + \
               struct.pack('<ff', 1.0, 0.0) + \
               struct.pack('<I', 0)

    assert result == expected


def test_deserialize_insufficient_header():
    """Test de désérialisation avec en-tête insuffisant."""
    data = b'\x00\x01'
    with pytest.raises(ValueError):
        deserialize_point_set(data)
