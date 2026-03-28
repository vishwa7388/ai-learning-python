package com.example.dispensingpharmacies.rule;

import java.util.Map;
import org.springframework.stereotype.Component;

@Component
public class QOHRule {

  public boolean passes(Map<String, Object> inventory) {
    if (inventory == null) {
      return false;
    }
    Object available = inventory.get("available");
    if (available instanceof Boolean b) {
      return b;
    }
    return true;
  }
}
