```mermaid
erDiagram
    users {
        VARCHAR(36) id PK
        DATETIME created_at
        DATETIME updated_at
        VARCHAR(50) first_name
        VARCHAR(50) last_name
        VARCHAR(120) email
        VARCHAR(128) password
        BOOLEAN is_admin
    }

    places {
        VARCHAR(36) id PK
        DATETIME created_at
        DATETIME updated_at
        VARCHAR(100) title
        TEXT description
        FLOAT price
        FLOAT latitude
        FLOAT longitude
        VARCHAR(36) owner_id FK
    }

    reviews {
        VARCHAR(36) id PK
        DATETIME created_at
        DATETIME updated_at
        TEXT text
        INTEGER rating
        VARCHAR(36) place_id FK
        VARCHAR(36) user_id FK
    }

    amenities {
        VARCHAR(36) id PK
        DATETIME created_at
        DATETIME updated_at
        VARCHAR(50) name
    }

    place_amenity {
        VARCHAR(36) place_id PK, FK
        VARCHAR(36) amenity_id PK, FK
    }

    users ||--o{ places : "has / owns"
    users ||--o{ reviews : "writes"
    places ||--o{ reviews : "receives"
    places ||--o{ place_amenity : "contains"
    amenities ||--o{ place_amenity : "belongs to"