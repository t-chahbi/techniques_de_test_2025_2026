# 1. Introduction

Ce document constitue le plan de tests pour le projet de développement du micro-service Triangulator. L'objectif principal de ce projet est de mettre en œuvre une stratégie de test complète et pertinente avant même le développement de la logique métier, en suivant une approche "Test-First".

Ce plan a pour but de garantir la fiabilité, la justesse, la performance et la qualité globale du composant Triangulator en définissant les différents types de tests qui seront mis en place, les outils utilisés et la stratégie adoptée.

# 2. Périmètre des Tests

## 2.1. Inclus dans les tests

Le périmètre de ce plan de test se concentre exclusivement sur le composant Triangulator. Cela inclut :
- La logique métier principale : L'algorithme de triangulation lui-même.
- La sérialisation/désérialisation des données : La conversion des structures PointSet et Triangles depuis et vers leur format binaire.
- L'API HTTP : La validation du comportement des points d'accès exposés, leur conformité avec la spécification OpenAPI et la gestion des codes de retour HTTP.
- L'interaction avec les dépendances : Le comportement du Triangulator face aux différentes réponses (succès, erreurs) du service PointSetManager.

## 2.2. Exclus des tests

Les composants suivants sont considérés comme des dépendances externes et ne seront pas testés dans le cadre de ce projet :
- Le PointSetManager
- La Database
- Le Client

Pour tester l'interaction du Triangulator avec le PointSetManager, nous utiliserons un mock de ce service afin de simuler son comportement et de nous isoler de sa logique interne et de sa disponibilité.

# 3. Stratégie de Test

La stratégie s'articule autour de trois axes principaux : les tests de comportement, les tests de performance et l'assurance qualité du code.

## 3.1. Tests de Comportement (Unitaires et API)

Ces tests visent à valider la justesse fonctionnelle du service. Ils seront exécutés via la commande make unit_test.

### 3.1.1. Tests Unitaires

L'objectif est de valider les plus petites unités de code de manière isolée.

- Module de Triangulation :
    - Pourquoi : Pour s'assurer que l'algorithme de triangulation est mathématiquement correct.
    - Comment :
        - Cas nominaux : Fournir des ensembles de points simples (ex: 3 points formant un triangle, 4 points formant un carré) et vérifier que les triangles générés sont conformes au résultat attendu.
        - Cas limites (edge cases) :
            - Tester avec un PointSet contenant moins de 3 points (aucun triangle ne doit être retourné).
            - Tester avec des points colinéaires (ne devraient pas former un triangle entre eux).
            - Tester avec des points coïncidents (superposés).
- Module de Sérialisation/Désérialisation :
    - Pourquoi : Pour garantir l'intégrité des données échangées entre les services.
    - Comment :
        - Créer un objet (PointSet ou Triangles), le sérialiser en binaire, puis le désérialiser. Vérifier que l'objet résultant est identique à l'original.
        - Tester avec des données vides (0 points, 0 triangles).
        - Tenter de désérialiser des flux binaires malformés (longueur incorrecte, types de données erronés) pour s'assurer que des erreurs appropriées sont levées.

### 3.1.2. Tests d'API / Intégration

L'objectif est de tester le service dans son ensemble, de la requête HTTP entrante à la réponse, en incluant l'interaction avec le PointSetManager (qui sera mocké).

- Scénario "Happy Path" :
    - Pourquoi : Pour valider le flux nominal de l'application.
    - Comment :
        1. Le client envoie une requête GET /triangulate/{point_set_id}.
        2. Le mock du PointSetManager est configuré pour retourner un PointSet binaire valide lorsque le Triangulator le contacte.
        3. Vérifier que la réponse du Triangulator est un statut 200 OK et que le corps de la réponse contient une structure Triangles binaire valide et correcte.
- Scénarios d'Erreur et "Unhappy Paths" :
    - Pourquoi : Pour s'assurer que le service est robuste et gère les erreurs de manière prévisible.
    - Comment :
        - PointSetID inconnu : Le mock du PointSetManager retourne une erreur 404 Not Found. On vérifiera que le Triangulator propage cette erreur avec un statut 404.
        - PointSetManager indisponible : Le mock simule une erreur serveur (500 ou 503). On vérifiera que le Triangulator retourne une erreur appropriée (ex: 502 Bad Gateway).
        - Données corrompues : Le mock du PointSetManager retourne un PointSet binaire malformé. On vérifiera que le Triangulator gère l'erreur de désérialisation et retourne un 500 Internal Server Error.
        - Requête client invalide : Envoyer une requête avec une méthode HTTP incorrecte (ex: POST) pour vérifier que le service retourne un 405 Method Not Allowed.

## 3.2. Tests de Performance

Ces tests visent à mesurer l'efficacité des opérations coûteuses. Ils seront exécutés séparément via la commande make perf_test et marqués avec @pytest.mark.perf.

- Performance de l'algorithme de triangulation :
    - Pourquoi : Pour comprendre comment le temps de calcul évolue avec la taille des données.
    - Comment : Mesurer le temps d'exécution de la fonction de triangulation sur des PointSet de tailles variables (100, 1 000, 10 000, 100 000 points) et enregistrer les résultats.
- Performance de la sérialisation/désérialisation :
    - Pourquoi : Pour identifier d'éventuels goulots d'étranglement dans la manipulation des données.
    - Comment : Mesurer le temps nécessaire pour convertir de grandes structures PointSet et Triangles depuis et vers leur format binaire.

## 3.3. Qualité de Code et Documentation

- Couverture de code :
    - Pourquoi : Pour s'assurer que l'ensemble du code est bien exécuté par la suite de tests.
    - Comment : Utiliser coverage (via make coverage) avec pour objectif d'atteindre une couverture de 100%. Bien que cet objectif soit quantitatif, il nous poussera à tester chaque branche de notre code.
- Qualité et style du code (Linting) :
    - Pourquoi : Pour maintenir un code propre, lisible et cohérent.
    - Comment : Utiliser ruff (via make lint) avec les règles définies dans pyproject.toml. L'objectif est qu'aucune erreur ne soit rapportée.
- Documentation :
    - Pourquoi : Pour assurer la maintenabilité et la compréhension du code.
    - Comment : Rédiger des docstrings pour toutes les fonctions, classes et modules, conformément aux règles de ruff. La documentation sera ensuite générée en HTML avec pdoc3 (via make doc).

# 4. Outils

- Framework de test : pytest
- Framework web : flask
- Mesure de couverture : coverage
- Analyse de qualité de code : ruff
- Génération de documentation : pdoc3
- Gestionnaire de tâches : make