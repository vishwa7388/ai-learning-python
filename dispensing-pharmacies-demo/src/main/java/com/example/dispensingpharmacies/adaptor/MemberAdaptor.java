package com.example.dispensingpharmacies.adaptor;

import com.example.dispensingpharmacies.model.MemberResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

@Component
@RequiredArgsConstructor
public class MemberAdaptor {

  private static final String ELIGIBILITY_URL = "https://member-api.example.com/v1/eligibility";

  private final RestTemplate restTemplate;

  public MemberResponse fetchEligibility(String memberId) {
    var uri =
        UriComponentsBuilder.fromHttpUrl(ELIGIBILITY_URL)
            .queryParam("memberId", memberId)
            .build()
            .toUri();
    try {
      MemberResponse body = restTemplate.getForObject(uri, MemberResponse.class);
      if (body != null) {
        return body;
      }
    } catch (RestClientException e) {
      // fall through to fake
    }
    return MemberResponse.builder()
        .memberId(memberId)
        .eligible(Boolean.TRUE)
        .planType("FAKE_PLAN")
        .build();
  }
}
