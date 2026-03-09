# Dispensing Pharmacies API - Flow Analysis

**Files Analyzed:** 2

---

## 1. Overview
This API facilitates the routing of pharmacy orders to the most optimal pharmacy based on various rules and external data sources.

## 2. Entry Point
- **Controller**: `SearchController`
- **Endpoint**: `/dispensingPharmacies/search`
- **HTTP Method**: POST

## 3. Request
- **Request Body**: `SearchRequest`
  - `ndc` (String): National Drug Code
  - `patientId` (String): Patient identifier

## 4. Processing Flow
Step 1: Retrieve drug information from the `DrugAdaptor`.
Step 2: Fetch member information from the `MembershipAdaptor`.
Step 3: Get pharmacy routing data from the `RxRoutingAdaptor`.
Step 4: Apply business rules to determine the optimal pharmacy and other pharmacies.
Step 5: Return the search response.

## 5. External API Calls
| API Name | Purpose | Called From |
|----------|---------|-------------|
| Drug API | Fetch drug information based on NDC | `DrugAdaptor` |

## 6. Business Rules
1. **GAC Rule**: Applies geographical and administrative criteria to select the nearest pharmacy.
2. **QOH Rule**: Ensures the selected pharmacy has sufficient stock of the drug.
3. **DoD Override**: Overrides the GAC and QOH rules based on specific conditions.

## 7. Response
- **Response Body**: `SearchResponse`
  - `optimalPharmacy` (Pharmacy): The most optimal pharmacy for the order.
  - `otherPharmacies` (List<Pharmacy>): List of other pharmacies in the routing order.