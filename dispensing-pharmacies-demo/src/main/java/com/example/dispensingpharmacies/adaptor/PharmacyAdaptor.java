package com.example.dispensingpharmacies.adaptor;

import com.example.dispensingpharmacies.model.PharmacyResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

@Component
@RequiredArgsConstructor
public class PharmacyAdaptor {

  private static final String PHARMACY_URL = "https://pharmacy-api.example.com/v1/pharmacy";

  private final RestTemplate restTemplate;

  public PharmacyResponse fetchPharmacy(String npi) {
    var uri =
        UriComponentsBuilder.fromHttpUrl(PHARMACY_URL).queryParam("npi", npi).build().toUri();
    try {
      PharmacyResponse body = restTemplate.getForObject(uri, PharmacyResponse.class);
      if (body != null) {
        return body;
      }
    } catch (RestClientException e) {
      // fall through to fake
    }
    return PharmacyResponse.builder()
        .npi(npi)
        .name("Fake Pharmacy")
        .address("123 Demo St")
        .inNetwork(Boolean.TRUE)
        .build();
  }
}
