package com.example.dispensingpharmacies.rule;

import com.example.dispensingpharmacies.model.SearchRequest;
import org.springframework.stereotype.Component;

@Component
public class DoDOverrideRule {

  public boolean passes(SearchRequest request) {
    if (request == null || request.getBenefitType() == null) {
      return true;
    }
    return !request.getBenefitType().equalsIgnoreCase("DOD_BLOCKED");
  }
}
