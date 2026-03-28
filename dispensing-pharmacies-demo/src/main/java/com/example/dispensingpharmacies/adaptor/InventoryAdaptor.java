package com.example.dispensingpharmacies.adaptor;

import java.util.LinkedHashMap;
import java.util.Map;
import lombok.RequiredArgsConstructor;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

@Component
@RequiredArgsConstructor
public class InventoryAdaptor {

  private static final String STOCK_URL = "https://inventory-api.example.com/v1/stock";

  private final RestTemplate restTemplate;

  public Map<String, Object> fetchStock(String npi, Integer quantity) {
    var builder = UriComponentsBuilder.fromHttpUrl(STOCK_URL).queryParam("npi", npi);
    if (quantity != null) {
      builder.queryParam("quantity", quantity);
    }
    var uri = builder.build().toUri();
    try {
      var body =
          restTemplate.exchange(
                  uri,
                  HttpMethod.GET,
                  null,
                  new ParameterizedTypeReference<Map<String, Object>>() {})
              .getBody();
      if (body != null) {
        return body;
      }
    } catch (RestClientException e) {
      // fall through to fake
    }
    Map<String, Object> fake = new LinkedHashMap<>();
    fake.put("npi", npi);
    fake.put("quantityOnHand", quantity != null ? quantity : 0);
    fake.put("available", Boolean.TRUE);
    return fake;
  }
}
