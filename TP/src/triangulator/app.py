"""Application Flask pour le micro-service Triangulator.

Ce module définit l'API HTTP du service de triangulation,
permettant de calculer la triangulation de Delaunay pour un
ensemble de points identifié par son ID.
"""

import os

import requests
from flask import Flask, Response, jsonify

from src.triangulator.core import triangulate
from src.triangulator.serialization import (
    deserialize_point_set,
    serialize_triangles,
)


def create_app(psm_url: str | None = None) -> Flask:
    """Crée et configure l'application Flask.

    Args:
        psm_url: URL de base du PointSetManager. Si None, utilise
                 la variable d'environnement PSM_URL ou localhost:5001.

    Returns:
        Flask: L'application Flask configurée.
    """
    app = Flask(__name__)

    if psm_url is None:
        psm_url = os.environ.get('PSM_URL', 'http://localhost:5001')

    app.config['PSM_URL'] = psm_url

    @app.route('/triangulation/<point_set_id>', methods=['GET'])
    def triangulate_endpoint(point_set_id: str) -> Response | tuple:
        """Calcule la triangulation pour un PointSet donné.

        Args:
            point_set_id: L'identifiant UUID du PointSet à trianguler.

        Returns:
            Response: La triangulation au format binaire (200),
                      ou une erreur JSON avec le code approprié.
        """
        psm_base_url = app.config['PSM_URL']

        try:
            psm_response = requests.get(
                f"{psm_base_url}/pointset/{point_set_id}",
                timeout=30
            )
        except requests.exceptions.RequestException:
            return jsonify({
                'code': 'PSM_UNAVAILABLE',
                'message': 'Le PointSetManager est indisponible.'
            }), 503

        if psm_response.status_code == 404:
            return jsonify({
                'code': 'NOT_FOUND',
                'message': f'PointSet {point_set_id} non trouvé.'
            }), 404

        if psm_response.status_code != 200:
            return jsonify({
                'code': 'PSM_ERROR',
                'message': 'Erreur du PointSetManager.'
            }), 502

        try:
            point_set = deserialize_point_set(psm_response.content)
        except ValueError as e:
            return jsonify({
                'code': 'INVALID_DATA',
                'message': f'Données PointSet invalides: {e}'
            }), 500

        try:
            triangles = triangulate(point_set)
        except Exception as e:
            return jsonify({
                'code': 'TRIANGULATION_FAILED',
                'message': f'Échec de la triangulation: {e}'
            }), 500

        result = serialize_triangles(point_set, triangles)

        return Response(result, status=200, mimetype='application/octet-stream')

    return app


if __name__ == '__main__':
    application = create_app()
    application.run(port=5002)
