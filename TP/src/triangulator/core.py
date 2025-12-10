"""Module principal de triangulation.

Ce module implémente l'algorithme de triangulation de Delaunay
en utilisant l'approche Bowyer-Watson incrémentale.
"""

import math


def _distance(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """Calcule la distance euclidienne entre deux points.

    Args:
        p1: Premier point (x, y).
        p2: Second point (x, y).

    Returns:
        float: La distance entre les deux points.
    """
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def _circumcircle(
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float]
) -> tuple[tuple[float, float], float] | None:
    """Calcule le cercle circonscrit d'un triangle.

    Args:
        p1: Premier sommet du triangle.
        p2: Deuxième sommet du triangle.
        p3: Troisième sommet du triangle.

    Returns:
        tuple: (centre, rayon) du cercle circonscrit, ou None si les points
               sont colinéaires.
    """
    ax, ay = p1
    bx, by = p2
    cx, cy = p3

    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))

    if abs(d) < 1e-10:
        return None

    ux = (
        (ax * ax + ay * ay) * (by - cy) +
        (bx * bx + by * by) * (cy - ay) +
        (cx * cx + cy * cy) * (ay - by)
    ) / d

    uy = (
        (ax * ax + ay * ay) * (cx - bx) +
        (bx * bx + by * by) * (ax - cx) +
        (cx * cx + cy * cy) * (bx - ax)
    ) / d

    center = (ux, uy)
    radius = _distance(center, p1)

    return (center, radius)


def _point_in_circumcircle(
    point: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float]
) -> bool:
    """Vérifie si un point est dans le cercle circonscrit d'un triangle.

    Args:
        point: Le point à tester.
        p1: Premier sommet du triangle.
        p2: Deuxième sommet du triangle.
        p3: Troisième sommet du triangle.

    Returns:
        bool: True si le point est dans le cercle circonscrit.
    """
    circle = _circumcircle(p1, p2, p3)
    if circle is None:
        return False

    center, radius = circle
    return _distance(point, center) < radius


def _are_collinear(points: list[tuple[float, float]]) -> bool:
    """Vérifie si tous les points sont colinéaires.

    Args:
        points: Liste de points à vérifier.

    Returns:
        bool: True si tous les points sont colinéaires.
    """
    if len(points) < 3:
        return True

    x1, y1 = points[0]
    x2, y2 = points[1]

    for i in range(2, len(points)):
        x3, y3 = points[i]
        cross = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
        if abs(cross) > 1e-10:
            return False

    return True


def _has_duplicates(points: list[tuple[float, float]]) -> bool:
    """Vérifie si la liste contient des points dupliqués/coïncidents.

    Args:
        points: Liste de points à vérifier.

    Returns:
        bool: True si des points sont coïncidents.
    """
    seen = set()
    for p in points:
        rounded = (round(p[0], 10), round(p[1], 10))
        if rounded in seen:
            return True
        seen.add(rounded)
    return False


def triangulate(
    point_set: list[tuple[float, float]]
) -> list[tuple[int, int, int]]:
    """Triangule un ensemble de points avec l'algorithme de Bowyer-Watson.

    Args:
        point_set: Liste de points (x, y) à trianguler.

    Returns:
        list: Liste de tuples (i1, i2, i3) représentant les indices des
              sommets de chaque triangle dans le point_set original.
    """
    if len(point_set) < 3:
        return []

    if _are_collinear(point_set) or _has_duplicates(point_set):
        return []

    min_x = min(p[0] for p in point_set)
    max_x = max(p[0] for p in point_set)
    min_y = min(p[1] for p in point_set)
    max_y = max(p[1] for p in point_set)

    dx = max_x - min_x
    dy = max_y - min_y
    delta_max = max(dx, dy)
    mid_x = (min_x + max_x) / 2
    mid_y = (min_y + max_y) / 2

    st_p1 = (mid_x - 20 * delta_max, mid_y - delta_max)
    st_p2 = (mid_x, mid_y + 20 * delta_max)
    st_p3 = (mid_x + 20 * delta_max, mid_y - delta_max)

    n = len(point_set)
    vertices = list(point_set) + [st_p1, st_p2, st_p3]

    triangles = [(n, n + 1, n + 2)]

    for i, point in enumerate(point_set):
        bad_triangles = []

        for tri in triangles:
            p1, p2, p3 = vertices[tri[0]], vertices[tri[1]], vertices[tri[2]]
            if _point_in_circumcircle(point, p1, p2, p3):
                bad_triangles.append(tri)

        polygon = []
        for tri in bad_triangles:
            edges = [
                (tri[0], tri[1]),
                (tri[1], tri[2]),
                (tri[2], tri[0])
            ]
            for edge in edges:
                edge_reversed = (edge[1], edge[0])
                is_shared = False
                for other_tri in bad_triangles:
                    if other_tri == tri:
                        continue
                    other_edges = [
                        (other_tri[0], other_tri[1]),
                        (other_tri[1], other_tri[2]),
                        (other_tri[2], other_tri[0])
                    ]
                    if edge in other_edges or edge_reversed in other_edges:
                        is_shared = True
                        break
                if not is_shared:
                    polygon.append(edge)

        for tri in bad_triangles:
            triangles.remove(tri)

        for edge in polygon:
            triangles.append((edge[0], edge[1], i))

    result = []
    for tri in triangles:
        if tri[0] < n and tri[1] < n and tri[2] < n:
            result.append(tri)

    return result
