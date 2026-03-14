package com.cigna.dp.service;

import org.springframework.stereotype.Component;

@Component
public class DoDOverrideRule {
    public String applyRule(SearchRequest req) { 
        // Condition: Retail hai toh chalega, Mail hai toh skip hoga
        if ("RETAIL".equalsIgnoreCase(req.getBenefitType())) {
            return "Department of Defense Override Applied for Retail";
        } else {
            return "Rule Skipped - Mail Benefit Not Eligible for DoD";
        }
    }
}
