# DP API Documentation

## Core Components
- **Controllers**: `SearchController`
- **Services**: `SearchService`
- **Rules**: `GACRule`, `QOHRule`, `DoDOverrideRule`

## Business Rules Applied
1. **Geographic Access Criteria (GAC)**: Ensures that the pharmacy is within an acceptable geographic distance.
2. **Quantity On Hand (QOH)**: Checks if the requested medication is in stock at the pharmacy.
3. **Department of Defense Override**: Allows access if the request is coming from a military department.

## Flow Summary
1. A `POST` request is made to `/dispensingPharmacies/search` with a `SearchRequest` body.
2. The `SearchController` receives the request and delegates it to the `SearchService`.
3. The `SearchService` applies the following rules in sequence:
   - `GACRule`: Validates if the pharmacy meets the geographic criteria.
   - `QOHRule`: Checks if the requested medication is in stock.
   - `DoDOverrideRule`: Overrides the rules if the request is from a military department.
4. If all rules pass, the service returns the optimal pharmacy (`Pharmacy_CVS_12345` in this mock response).