"""Tests d'API pour le micro-service Triangulator."""

import struct
from unittest.mock import Mock, patch

import pytest


@pytest.fixture
def mock_requests_get():
    """Fixture pour mocker requests.get."""
    with patch('src.triangulator.app.requests.get') as mock_get:
        yield mock_get


def test_triangulate_happy_path(client, mock_requests_get):
    """Test du scénario nominal: triangulation réussie."""
    point_set_data = struct.pack('L', 3) + \
                     struct.pack('ff', 0.0, 0.0) + \
                     struct.pack('ff', 1.0, 0.0) + \
                     struct.pack('ff', 0.0, 1.0)

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = point_set_data
    mock_requests_get.return_value = mock_response

    response = client.get('/triangulation/123e4567-e89b-12d3-a456-426614174000')

    assert response.status_code == 200
    assert len(response.data) > 0


def test_triangulate_psm_not_found(client, mock_requests_get):
    """Test du cas où le PointSet n'est pas trouvé."""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_requests_get.return_value = mock_response

    response = client.get('/triangulation/unknown-id')
    assert response.status_code == 404


def test_triangulate_psm_error(client, mock_requests_get):
    """Test du cas où le PSM retourne une erreur."""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_requests_get.return_value = mock_response

    response = client.get('/triangulation/error-id')
    assert response.status_code == 502


def test_triangulate_invalid_method(client):
    """Test d'une méthode HTTP invalide."""
    response = client.post('/triangulation/123')
    assert response.status_code == 405


def test_triangulate_psm_unavailable(client, mock_requests_get):
    """Test du cas où le PSM est indisponible."""
    import requests
    mock_requests_get.side_effect = requests.exceptions.ConnectionError()

    response = client.get('/triangulation/some-id')
    assert response.status_code == 503


def test_triangulate_empty_point_set(client, mock_requests_get):
    """Test avec un PointSet vide."""
    point_set_data = struct.pack('L', 0)

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = point_set_data
    mock_requests_get.return_value = mock_response

    response = client.get('/triangulation/empty-set')
    assert response.status_code == 200
