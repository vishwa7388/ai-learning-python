package com.cigna.dp.service;

import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class SearchService {

    // Injecting 3 active rules
    private final GACRule gacRule;
    private final QOHRule qohRule;
    private final DoDOverrideRule dodOverrideRule;

    public SearchService(GACRule gacRule, QOHRule qohRule, DoDOverrideRule dodOverrideRule) {
        this.gacRule = gacRule;
        this.qohRule = qohRule;
        this.dodOverrideRule = dodOverrideRule;
    }

    public String findOptimalPharmacy(SearchRequest request) {
        System.out.println("Fetching pharmacies from RxRouting Adaptor...");
        
        // Applying Business Rules
        System.out.println("Applying Rule 1: " + gacRule.applyRule(request));
        System.out.println("Applying Rule 2: " + qohRule.applyRule(request));
        System.out.println("Applying Rule 3: " + dodOverrideRule.applyRule(request));
        
        return "Pharmacy_CVS_12345"; // Mock response
    }
}