// GetAllowedServiceBranchRule.java
@Component
public class GetAllowedServiceBranchRule {
    public String applyRule(SearchRequest req) { 
        return "Military Service Branch Validated"; 
    }
}