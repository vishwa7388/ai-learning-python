## 1. Overview
The Dispensing Pharmacies API is a microservice designed to route pharmacy requests based on business rules such as benefit type, geographic access criteria, and military service branch validation.

## 2. Entry Point
- **Controller:** `SearchController`
- **Endpoint:** `/dispensingPharmacies/search`
- **HTTP Method:** POST

## 3. Request
### Fields:
- `benefitType` (String): Must be either "RETAIL" or "MAIL"

## 4. Processing Flow
1. The `SearchController` receives the request.
2. The `SearchService` processes the request by applying various business rules sequentially.

## 5. External API Calls
| API Name | Purpose | Called From |
|----------|---------|-------------|
| N/A      | N/A     | N/A         |

## 6. Business Rules
1. **DoDOverrideRule**: Checks if the `benefitType` is "RETAIL". If true, applies a Department of Defense override; otherwise, skips this rule.
2. **GACRule**: Validates that geographic access criteria are met.
3. **QOHRule**: Ensures that the quantity on hand (QOH) is sufficient.
4. **GetAllowedServiceBranchRule**: Verifies if the military service branch in the request is valid.

## 7. Response
- The response will be a string indicating either the optimal pharmacy or a message regarding skipped rules based on business logic application.