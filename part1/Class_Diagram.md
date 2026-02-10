# Business Logic Layer - Class Diagram Explanatory Notes

## 1. Introduction
This diagram details the entities in the Business Logic Layer. It defines the attributes and methods for each model, serving as a blueprint for the Python classes.

## 2. Entities Description
* **User:** Represents a registered user. Attributes include personal info (email, name) and system info (is_admin).
* **Place:** Represents a property listing. It is linked to a `User` (owner) and can have multiple `Amenities`.
* **Review:** Represents feedback left by a `User` on a `Place`.
* **Amenity:** Represents features of a place (e.g., Wifi, Pool).

## 3. Relationships
* **User - Place:** One-to-Many. A user can own multiple places.
* **User - Review:** One-to-Many. A user can write multiple reviews.
* **Place - Review:** One-to-Many. A place can receive multiple reviews.
* **Place - Amenity:** Many-to-Many. A place can have many amenities, and an amenity can belong to many places.
