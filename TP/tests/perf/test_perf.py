import pytest
import time
import struct
from src.triangulator.core import triangulate
from src.triangulator.serialization import serialize_point_set, deserialize_point_set

@pytest.mark.perf
def test_triangulation_performance():
    # Generate a large point set
    points = [(float(i), float(i)) for i in range(1000)]
    
    start_time = time.time()
    try:
        triangulate(points)
    except NotImplementedError:
        pytest.skip("Triangulation not implemented yet")
    end_time = time.time()
    
    duration = end_time - start_time
    # Just logging the duration, or asserting it's under a threshold
    print(f"Triangulation of 1000 points took {duration} seconds")

@pytest.mark.perf
def test_serialization_performance():
    points = [(float(i), float(i)) for i in range(10000)]
    
    start_time = time.time()
    try:
        data = serialize_point_set(points)
        deserialize_point_set(data)
    except NotImplementedError:
        pytest.skip("Serialization not implemented yet")
    end_time = time.time()
    
    duration = end_time - start_time
    print(f"Serialization/Deserialization of 10000 points took {duration} seconds")
