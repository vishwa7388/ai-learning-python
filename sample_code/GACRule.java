// GACRule.java
@Component
public class GACRule {
    public String applyRule(SearchRequest req) { return "Geographic Access Criteria Passed"; }
}

// QOHRule.java
@Component
public class QOHRule {
    public String applyRule(SearchRequest req) { return "Quantity On Hand Checked"; }
}
