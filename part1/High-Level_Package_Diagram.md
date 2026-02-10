# High-Level Package Diagram - Explanatory Notes

## 1. Presentation Layer (Services & API)
This layer handles the interaction between the user and the application (HTTP requests). It does not contain business logic but delegates commands to the Business Logic Layer via the Facade.

## 2. Business Logic Layer (Models)
This layer contains the core logic and data models:
* **Models:** User, Place, Review, Amenity.
* **HBnBFacade:** This pattern provides a simplified interface for the Presentation Layer. It hides the complexity of the underlying subsystems (models and storage).

## 3. Persistence Layer (Data Storage)
This layer is responsible for storing and retrieving data. The Business Logic Layer interacts with it to persist objects (save to JSON files or Database).
