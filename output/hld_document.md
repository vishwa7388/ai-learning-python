## System Overview
This Spring Boot microservice system provides a search functionality for dispensed medications, integrating with multiple external APIs to retrieve benefits, inventory, member eligibility, and pharmacy details.

## Architecture Layers
- **Controller**: Handles incoming HTTP requests.
- **Service**: Orchestrates business logic by calling multiple adaptors.
- **Adaptor**: Communicates with external systems to fetch data.
- **Model**: Represents data structures used within the service.

## Component Responsibilities
| Component | Layer | Responsibility |
|-----------|-------|----------------|
| `DispensingPharmaciesDemoApplication` | N/A | Bootstraps the application. |
| `BenefitAdaptor`, `InventoryAdaptor`, `MemberAdaptor`, `NotificationAdaptor`, `PharmacyAdaptor` | Adaptor | Fetches data from external APIs. |
| `RestTemplateConfig` | Configuration | Configures `RestTemplate` for HTTP requests. |
| `BenefitController`, `MemberController`, `PharmacyController`, `SearchController` | Controller | Processes incoming requests and returns responses. |
| `PharmacyService` | Service | Orchestrates business logic, coordinating with adaptors. |
| `SearchService` | Service | Handles the main search functionality, applying rules and integrating multiple adaptors. |
| `DoDOverrideRule`, `GACRule`, `QOHRule` | Rule | Defines specific rules for search validation. |
| `MemberResponse`, `PharmacyResponse`, `SearchRequest` | Model | Represents data structures used within the service. |

## External Systems and APIs
| System/API | Purpose | Called From |
|------------|---------|-------------|
| benefit-api.example.com | Fetches benefits based on member ID. | BenefitAdaptor |
| inventory-api.example.com | Fetches stock details for a pharmacy NPI. | InventoryAdaptor |
| member-api.example.com | Checks member eligibility and plan type. | MemberAdaptor |
| notify-api.example.com | Sends notifications about search events. | NotificationAdaptor |
| pharmacy-api.example.com | Retrieves pharmacy details based on NPI. | PharmacyAdaptor |

## Tech Stack
- Spring Boot
- Java 8+
- Maven/Gradle for build management
- JUnit for testing

This system is designed to be highly modular, making it easy to integrate and extend in the future.