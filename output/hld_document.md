## System Overview
The Dispensing Pharmacies API is a pharmacy routing microservice that determines the optimal pharmacy based on search criteria, applying various rules and checks to ensure eligibility.

## Architecture Layers
- **Controller**: Handles incoming HTTP requests.
- **Service**: Orchestrates the business logic by calling rules.
- **Adaptor (or Adapter)**: Not explicitly present in the code.
- **Model**: Contains the data structure for search requests.

## Component Responsibilities
| Component          | Layer   | Responsibility                                                                 |
|--------------------|---------|--------------------------------------------------------------------------------|
| SearchController   | Controller | Handles incoming search requests and invokes the service to find the optimal pharmacy. |
| SearchService      | Service  | Orchestrates rule application and determines the optimal pharmacy.                |
| DoDOverrideRule    | Service  | Applies Department of Defense override rules based on benefit type.               |
| GACRule            | Service  | Validates Geographic Access Criteria for the request.                           |
| QOHRule            | Service  | Checks Quantity On Hand for inventory availability.                             |
| GetAllowedServiceBranchRule | Service | Ensures that the military service branch is valid for the request.              |
| SearchRequest      | Model    | Represents the search criteria including benefit type.                         |

## External Systems and APIs
| System/API        | Purpose                          | Called From                    |
|-------------------|----------------------------------|--------------------------------|
| None              | No external systems or APIs are called within the provided code. |

## Tech Stack
- **Language**: Java
- **Framework**: Spring Boot
- **Key Libraries**: None explicitly listed in the provided code.
- **Build Tool**: Maven (inferred from the structure of the project)

## Data Flow Summary
1. A `SearchRequest` is received by the `SearchController`.
2. The `SearchService` is invoked to determine the optimal pharmacy.
3. Various rules (`DoDOverrideRule`, `GACRule`, etc.) are applied sequentially.
4. The service processes the rules and returns the optimal pharmacy.
5. The `SearchController` responds with the result.

This concise high-level design outlines the core components, their responsibilities, and the flow of data through the system.