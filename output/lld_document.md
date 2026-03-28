## Class dependency overview
- **SearchController** calls **SearchService**
- **SearchService** calls multiple rule classes: **DoDOverrideRule**, **GACRule**, **QOHRule**, and **GetAllowedServiceBranchRule**

## SearchController
### Key fields / attributes
- None

### Methods
| Method | Parameters | Return type | Purpose |
|--------|------------|-------------|---------|
| search | @RequestBody SearchRequest request | ResponseEntity<String> | Handles the POST request to find the optimal pharmacy |

### Dependencies
- **SearchService**

## SearchService
### Key fields / attributes
- None

### Methods
| Method | Parameters | Return type | Purpose |
|--------|------------|-------------|---------|
| findOptimalPharmacy | SearchRequest req | String | Determines the optimal pharmacy based on rules |

### Dependencies
- **DoDOverrideRule**
- **GACRule**
- **QOHRule**
- **GetAllowedServiceBranchRule**

## DoDOverrideRule
### Key fields / attributes
- None

### Methods
| Method | Parameters | Return type | Purpose |
|--------|------------|-------------|---------|
| applyRule | SearchRequest req | String | Applies the Department of Defense override rule |

### Dependencies
- None

## GACRule
### Key fields / attributes
- None

### Methods
| Method | Parameters | Return type | Purpose |
|--------|------------|-------------|---------|
| applyRule | SearchRequest req | String | Checks if the Geographic Access Criteria is passed |

### Dependencies
- None

## QOHRule
### Key fields / attributes
- None

### Methods
| Method | Parameters | Return type | Purpose |
|--------|------------|-------------|---------|
| applyRule | SearchRequest req | String | Verifies if the Quantity On Hand check passes |

### Dependencies
- None

## GetAllowedServiceBranchRule
### Key fields / attributes
- None

### Methods
| Method | Parameters | Return type | Purpose |
|--------|------------|-------------|---------|
| applyRule | SearchRequest req | String | Validates if the Military Service Branch is valid |

### Dependencies
- None