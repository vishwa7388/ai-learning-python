package com.example.dispensingpharmacies.rule;

import com.example.dispensingpharmacies.model.SearchRequest;
import org.springframework.stereotype.Component;

@Component
public class GACRule {

  public boolean passes(SearchRequest request) {
    if (request == null || request.getQuantity() == null) {
      return true;
    }
    return request.getQuantity() > 0 && request.getQuantity() <= 90;
  }
}
