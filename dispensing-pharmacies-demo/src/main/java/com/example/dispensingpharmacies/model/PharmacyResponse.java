package com.example.dispensingpharmacies.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PharmacyResponse {

  private String npi;
  private String name;
  private String address;
  private Boolean inNetwork;
}
