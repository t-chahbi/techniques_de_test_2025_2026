import pytest
import struct
from src.triangulator.serialization import serialize_point_set, deserialize_point_set, serialize_triangles

def test_serialize_point_set_nominal():
    points = [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)]
    # Expected binary:
    # Count (3) - 4 bytes
    # (0.0, 0.0) - 8 bytes
    # (1.0, 1.0) - 8 bytes
    # (2.0, 2.0) - 8 bytes
    expected = struct.pack('L', 3) + \
               struct.pack('ff', 0.0, 0.0) + \
               struct.pack('ff', 1.0, 1.0) + \
               struct.pack('ff', 2.0, 2.0)
    
    assert serialize_point_set(points) == expected

def test_deserialize_point_set_nominal():
    data = struct.pack('L', 3) + \
           struct.pack('ff', 0.0, 0.0) + \
           struct.pack('ff', 1.0, 1.0) + \
           struct.pack('ff', 2.0, 2.0)
    
    expected = [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)]
    assert deserialize_point_set(data) == expected

def test_serialize_deserialize_round_trip():
    points = [(1.5, 2.5), (-1.0, 0.0)]
    serialized = serialize_point_set(points)
    deserialized = deserialize_point_set(serialized)
    assert deserialized == points

def test_serialize_empty_point_set():
    points = []
    expected = struct.pack('L', 0)
    assert serialize_point_set(points) == expected
    assert deserialize_point_set(expected) == points

def test_deserialize_malformed_data_length():
    # Data too short
    data = struct.pack('L', 1) # Says 1 point but no point data
    with pytest.raises(ValueError):
        deserialize_point_set(data)

def test_serialize_triangles_nominal():
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    triangles = [(0, 1, 2)]
    
    # PointSet part
    expected = struct.pack('L', 3) + \
               struct.pack('ff', 0.0, 0.0) + \
               struct.pack('ff', 1.0, 0.0) + \
               struct.pack('ff', 0.0, 1.0)
    
    # Triangles part
    expected += struct.pack('L', 1) + \
                struct.pack('LLL', 0, 1, 2)
                
    assert serialize_triangles(points, triangles) == expected
