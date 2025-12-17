# Retour d'Expérience - TP Techniques de Test

**Auteur:** Thaha CHAHBI  
**Date:** Décembre 2025

## 1. Bilan Global

Ce TP m'a permis de mettre en pratique une approche de développement "Test-First" dans le cadre de la réalisation d'un micro-service de triangulation. Le travail a été structuré en plusieurs phases distinctes : planification, mise en place des tests, puis implémentation.

## 2. Ce qui a bien fonctionné

### 2.1. La Phase de Planification

L'élaboration du plan de tests en amont (PLAN.md) a été très bénéfique. En réfléchissant aux tests avant d'écrire le code, j'ai pu :
- Identifier clairement les cas limites à gérer (points colinéaires, coïncidents, moins de 3 points)
- Définir précisément les comportements attendus de l'API
- Anticiper les scénarios d'erreur (PSM indisponible, données corrompues)

### 2.2. La Structure des Tests

L'organisation des tests en trois catégories (unitaires, API, performance) avec des marqueurs pytest s'est avérée efficace :
- Les tests unitaires valident chaque fonction de manière isolée
- Les tests d'API vérifient le comportement bout-en-bout avec mocking du PSM
- Les tests de performance sont exécutables séparément pour éviter de ralentir le cycle de développement

### 2.3. L'Utilisation des Mocks

Le mocking du PointSetManager a permis de tester l'API de manière isolée et reproductible, sans dépendance sur un service externe.

## 3. Ce qui aurait pu être mieux fait

### 3.1. Tests d'Intégration

Le projet manque de tests d'intégration réels avec un PointSetManager "bouchonné" tournant en local. Les mocks de requests.get sont suffisants mais ne testent pas le comportement réel du réseau.

### 3.2. Algorithme de Triangulation

L'implémentation de l'algorithme Bowyer-Watson est fonctionnelle mais pourrait être optimisée :
- La complexité actuelle est O(n²) dans le pire cas
- Un arbre de recherche spatial améliorerait significativement les performances sur de grands ensembles

### 3.3. Gestion des Erreurs

Certains cas d'erreur pourraient être mieux documentés et testés, notamment :
- Validation du format UUID pour les point_set_id
- Limites de taille des PointSet acceptés

## 4. Points Clés Appris

1. **Test-First fonctionne** : Écrire les tests d'abord force à réfléchir à l'interface et aux cas limites avant de s'enliser dans l'implémentation.

2. **La couverture n'est pas tout** : 100% de couverture ne garantit pas des tests pertinents. La qualité des assertions est plus importante que le pourcentage.

3. **Documentation intégrée** : L'obligation de documenter (via ruff/pydocstyle) améliore la maintenabilité et force à clarifier sa pensée.

## 5. Améliorations Futures

Si je devais continuer ce projet :
- Ajouter des tests de propriété (property-based testing) avec Hypothesis
- Implémenter un cache pour les triangulations déjà calculées
- Ajouter des métriques de performance (temps de réponse, taille des réponses)
- Mettre en place une CI/CD avec GitHub Actions

## Conclusion

Ce TP a renforcé ma conviction que l'approche Test-First, bien que demandant un investissement initial plus important, permet d'aboutir à un code plus robuste et mieux conçu. Le fait de devoir réfléchir aux tests avant l'implémentation conduit naturellement à une meilleure architecture et une meilleure gestion des cas limites.
