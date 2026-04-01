## Class dependency overview

- `DispensingPharmaciesDemoApplication` calls no other classes.
- `BenefitAdaptor`, `InventoryAdaptor`, `MemberAdaptor`, `NotificationAdaptor`, and `PharmacyAdaptor` are called by various controllers and services.
- `RestTemplateConfig` provides a single instance of `RestTemplate`.
- `BenefitController`, `MemberController`, `PharmacyController`, and `SearchController` call respective adaptors.
- `PharmacyService` calls the `PharmacyAdaptor`.
- `SearchService` calls multiple adaptors (`MemberAdaptor`, `PharmacyAdaptor`, `BenefitAdaptor`, `InventoryAdaptor`, `NotificationAdaptor`) and rules.

## BenefitAdaptor

### Key fields / attributes
- `restTemplate`: Injected by Spring; used to make HTTP requests.

### Methods
| Method | Parameters | Return type | Purpose |
|--------|------------|-------------|---------|
| fetchBenefits(String memberId) | `memberId` (String) | Map<String, Object> | Fetches benefits for a given member ID. Falls back to a fake response on failure. |

### Dependencies
- `RestTemplate`

## InventoryAdaptor

### Key fields / attributes
- `restTemplate`: Injected by Spring; used to make HTTP requests.

### Methods
| Method | Parameters | Return type | Purpose |
|--------|------------|-------------|---------|
| fetchStock(String npi, Integer quantity) | `npi` (String), `quantity` (Integer) | Map<String, Object> | Fetches stock information for a given NPI and optional quantity. Falls back to a fake response on failure. |

### Dependencies
- `RestTemplate`

## MemberAdaptor

### Key fields / attributes
- `restTemplate`: Injected by Spring; used to make HTTP requests.

### Methods
| Method | Parameters | Return type | Purpose |
|--------|------------|-------------|---------|
| fetchEligibility(String memberId) | `memberId` (String) | MemberResponse | Fetches eligibility information for a given member ID. |

### Dependencies
- `RestTemplate`

## NotificationAdaptor

### Key fields / attributes
- `restTemplate`: Injected by Spring; used to make HTTP requests.

### Methods
| Method | Parameters | Return type | Purpose |
|--------|------------|-------------|---------|
| sendNotification(Map<String, Object> payload) | `payload` (Map<String, Object>) | Map<String, Object> | Sends a notification and returns the response. |

### Dependencies
- `RestTemplate`

## PharmacyAdaptor

### Key fields / attributes
- `restTemplate`: Injected by Spring; used to make HTTP requests.

### Methods
| Method | Parameters | Return type | Purpose |
|--------|------------|-------------|---------|
| fetchPharmacy(String npi) | `npi` (String) | PharmacyResponse | Fetches pharmacy details for a given NPI. |

### Dependencies
- `RestTemplate`

## RestTemplateConfig

### Key fields / attributes
- None

### Methods
| Method | Parameters | Return type | Purpose |
|--------|------------|-------------|---------|
| restTemplate() | - | RestTemplate | Provides an instance of `RestTemplate`. |

### Dependencies
- None

## BenefitController

### Key fields / attributes
- None

### Methods
| Method | Parameters | Return type | Purpose |
|--------|------------|-------------|---------|
| eligibility(String memberId) | `memberId` (String) | ResponseEntity<MemberResponse> | Handles requests for member eligibility. |

### Dependencies
- `BenefitAdaptor`

## MemberController

### Key fields / attributes
- None

### Methods
| Method | Parameters | Return type | Purpose |
|--------|------------|-------------|---------|
| eligibility(String memberId) | `memberId` (String) | ResponseEntity<MemberResponse> | Handles requests for member eligibility. |

### Dependencies
- `MemberAdaptor`

## PharmacyController

### Key fields / attributes
- None

### Methods
| Method | Parameters | Return type | Purpose |
|--------|------------|-------------|---------|
| getPharmacy(String npi) | `npi` (String) | ResponseEntity<PharmacyResponse> | Handles requests for pharmacy details. |

### Dependencies
- `PharmacyService`

## SearchController

### Key fields / attributes
- None

### Methods
| Method | Parameters | Return type | Purpose |
|--------|------------|-------------|---------|
| search(SearchRequest request) | `request` (SearchRequest) | ResponseEntity<Map<String, Object>> | Handles requests for searching data. |

### Dependencies
- `SearchService`

## MemberResponse

### Key fields / attributes
- `memberId`: String
- `eligible`: Boolean
- `planType`: String

### Methods
- Getter and Setter methods.

### Dependencies
- None

## PharmacyResponse

### Key fields / attributes
- `npi`: String
- `name`: String
- `address`: String
- `inNetwork`: Boolean

### Methods
- Getter and Setter methods.

### Dependencies
- None

## SearchRequest

### Key fields / attributes
- `memberId`: String
- `npi`: String
- `benefitType`: String
- `quantity`: Integer

### Methods
- Getter and Setter methods.

### Dependencies
- None

## DoDOverrideRule

### Key fields / attributes
- None

### Methods
| Method | Parameters | Return type | Purpose |
|--------|------------|-------------|---------|
| passes(SearchRequest request) | `request` (SearchRequest) | boolean | Checks if the DoD override rule is passed. |

### Dependencies
- None

## GACRule

### Key fields / attributes
- None

### Methods
| Method | Parameters | Return type | Purpose |
|--------|------------|-------------|---------|
| passes(SearchRequest request) | `request` (SearchRequest) | boolean | Checks if the GAC rule is passed. |

### Dependencies
- None

## QOHRule

### Key fields / attributes
- None

### Methods
| Method | Parameters | Return type | Purpose |
|--------|------------|-------------|---------|
| passes(Map<String, Object> inventory) | `inventory` (Map<String, Object>) | boolean | Checks if the QOH rule is passed. |

### Dependencies
- None

## PharmacyService

### Key fields / attributes
- None

### Methods
| Method | Parameters | Return type | Purpose |
|--------|------------|-------------|---------|
| getByNpi(String npi) | `npi` (String) | PharmacyResponse | Fetches pharmacy details by NPI. |

### Dependencies
- `PharmacyAdaptor`

## SearchService

### Key fields / attributes
- None

### Methods
| Method | Parameters | Return type | Purpose |
|--------|------------|-------------|---------|
| search(SearchRequest request) | `request` (SearchRequest) | Map<String, Object> | Searches data based on the provided request. |

### Dependencies
- `MemberAdaptor`, `PharmacyAdaptor`, `BenefitAdaptor`, `InventoryAdaptor`, `NotificationAdaptor`, `DoDOverrideRule`, `GACRule`, `QOHRule`