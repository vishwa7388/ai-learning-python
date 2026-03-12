```markdown
# Dispensing Pharmacies API Documentation

## Overview
This API routes pharmacy orders based on drug information and member details.

## Entry Point
- **Controller**: `SearchController`
- **Endpoint**: `/dispensingPharmacies/search`
- **HTTP Method**: `POST`

## Request
- **Request Body**: `SearchRequest`
  - `ndc` (String): National Drug Code
  - `patientId` (String): Member's unique identifier

## Processing Flow
1. Receive `SearchRequest`
2. Call `DrugAdaptor.getDrugInfo(ndc)` to retrieve drug information
3. Call `MembershipAdaptor.getMemberInfo(patientId)` to retrieve member details
4. Call `RxRoutingAdaptor.getRouting(drug, member)` to get a list of pharmacies
5. Apply business rules (GAC Rule, QOH Rule, DoD Override)
6. Return `SearchResponse` with optimal pharmacy and list of alternatives

## External API Calls
| API Name | Purpose | Called From |
|----------|---------|-------------|
| Drug API | Retrieves drug information | `DrugAdaptor.getDrugInfo(ndc)` |

## Business Rules
1. **GAC Rule**: Ensures the pharmacy is authorized to dispense the drug to the member.
2. **QOH Rule**: Validates that the pharmacy has the required quantity on hand.
3. **DoD Override**: Allows the pharmacy to override the default rules under certain conditions.

## Response
- **Response Body**: `SearchResponse`
  - `optimalPharmacy` (Pharmacy): The optimal pharmacy to dispense the drug
  - `alternativePharmacies` (List<Pharmacy>): A list of alternative pharmacies
```