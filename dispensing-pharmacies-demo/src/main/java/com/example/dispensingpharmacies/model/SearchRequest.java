package com.example.dispensingpharmacies.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class SearchRequest {

  private String memberId;
  private String npi;
  private String benefitType;
  private Integer quantity;
}
