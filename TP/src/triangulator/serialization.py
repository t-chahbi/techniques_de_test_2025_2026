"""Module de sérialisation/désérialisation pour PointSet et Triangles.

Ce module fournit les fonctions nécessaires pour convertir les structures
de données PointSet et Triangles depuis et vers leur format binaire,
tel que défini dans la spécification du projet.
"""

import struct


def serialize_point_set(point_set: list[tuple[float, float]]) -> bytes:
    """Sérialise un ensemble de points au format binaire.

    Le format binaire est:
    - 4 premiers bytes: unsigned int (32-bit) indiquant le nombre de points
    - Pour chaque point: 8 bytes (2 floats de 4 bytes pour X et Y)

    Args:
        point_set: Liste de tuples (x, y) représentant les points.

    Returns:
        bytes: La représentation binaire du PointSet.
    """
    count = len(point_set)
    result = struct.pack('<I', count)

    for x, y in point_set:
        result += struct.pack('<ff', x, y)

    return result


def deserialize_point_set(data: bytes) -> list[tuple[float, float]]:
    """Désérialise des bytes en liste de points.

    Args:
        data: La représentation binaire d'un PointSet.

    Returns:
        list: Liste de tuples (x, y) représentant les points.

    Raises:
        ValueError: Si les données sont malformées ou incomplètes.
    """
    if len(data) < 4:
        raise ValueError("Données insuffisantes pour le compteur de points")

    count = struct.unpack('<I', data[:4])[0]
    expected_size = 4 + count * 8

    if len(data) < expected_size:
        raise ValueError(
            f"Données incomplètes: attendu {expected_size} bytes, "
            f"reçu {len(data)} bytes"
        )

    points = []
    offset = 4

    for _ in range(count):
        x, y = struct.unpack('<ff', data[offset:offset + 8])
        points.append((x, y))
        offset += 8

    return points


def serialize_triangles(
    points: list[tuple[float, float]],
    triangles: list[tuple[int, int, int]]
) -> bytes:
    """Sérialise les triangles au format binaire.

    Le format binaire est composé de deux parties:
    1. Partie PointSet: sérialisation des sommets (identique à serialize_point_set)
    2. Partie Triangles:
       - 4 bytes: unsigned int (32-bit) pour le nombre de triangles
       - Pour chaque triangle: 12 bytes (3 unsigned ints pour les indices)

    Args:
        points: Liste des sommets (points).
        triangles: Liste de tuples (i1, i2, i3) représentant les indices
                   des sommets de chaque triangle.

    Returns:
        bytes: La représentation binaire des Triangles.
    """
    result = serialize_point_set(points)

    triangle_count = len(triangles)
    result += struct.pack('<I', triangle_count)

    for i1, i2, i3 in triangles:
        result += struct.pack('<III', i1, i2, i3)

    return result
