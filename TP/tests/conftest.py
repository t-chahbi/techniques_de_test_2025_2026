"""Configuration pytest pour les tests du Triangulator."""

import pytest

from src.triangulator.app import create_app


@pytest.fixture
def app():
    """Fixture pour créer l'application Flask en mode test."""
    application = create_app()
    application.config.update({
        "TESTING": True,
    })
    return application


@pytest.fixture
def client(app):
    """Fixture pour obtenir le client de test Flask."""
    return app.test_client()
