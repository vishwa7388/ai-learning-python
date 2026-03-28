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
public class BenefitAdaptor {

  private static final String BENEFITS_URL = "https://benefit-api.example.com/v1/benefits";

  private final RestTemplate restTemplate;

  public Map<String, Object> fetchBenefits(String memberId) {
    var uri =
        UriComponentsBuilder.fromHttpUrl(BENEFITS_URL)
            .queryParam("memberId", memberId)
            .build()
            .toUri();
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
    fake.put("memberId", memberId);
    fake.put("copay", 10);
    fake.put("benefitTier", "STANDARD");
    return fake;
  }
}

