import pytest
from unittest.mock import patch, Mock
import struct

@pytest.fixture
def mock_requests_get():
    with patch('requests.get') as mock_get:
        yield mock_get

def test_triangulate_happy_path(client, mock_requests_get):
    # Mock PSM response with a valid PointSet binary
    # 3 points: (0,0), (1,0), (0,1)
    point_set_data = struct.pack('L', 3) + \
                     struct.pack('ff', 0.0, 0.0) + \
                     struct.pack('ff', 1.0, 0.0) + \
                     struct.pack('ff', 0.0, 1.0)
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = point_set_data
    mock_requests_get.return_value = mock_response

    response = client.get('/triangulate/123')
    
    assert response.status_code == 200
    # Response should be binary Triangles
    # We expect at least the header (count points + points + count triangles)
    assert len(response.data) > 0

def test_triangulate_psm_not_found(client, mock_requests_get):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_requests_get.return_value = mock_response

    response = client.get('/triangulate/unknown')
    assert response.status_code == 404

def test_triangulate_psm_error(client, mock_requests_get):
    mock_response = Mock()
    mock_response.status_code = 500
    mock_requests_get.return_value = mock_response

    response = client.get('/triangulate/error')
    # Should return 502 Bad Gateway or 500
    assert response.status_code in [500, 502]

def test_triangulate_invalid_method(client):
    response = client.post('/triangulate/123')
    assert response.status_code == 405
