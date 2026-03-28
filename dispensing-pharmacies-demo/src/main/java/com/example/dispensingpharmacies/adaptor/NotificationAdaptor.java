package com.example.dispensingpharmacies.adaptor;

import java.util.LinkedHashMap;
import java.util.Map;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

@Component
@RequiredArgsConstructor
public class NotificationAdaptor {

  private static final String SEND_URL = "https://notify-api.example.com/v1/send";

  private final RestTemplate restTemplate;

  public Map<String, Object> sendNotification(Map<String, Object> payload) {
    var headers = new HttpHeaders();
    headers.setContentType(MediaType.APPLICATION_JSON);
    var entity = new HttpEntity<>(payload, headers);
    try {
      @SuppressWarnings("unchecked")
      Map<String, Object> body = restTemplate.postForObject(SEND_URL, entity, Map.class);
      return body != null ? body : Map.of("status", "UNKNOWN");
    } catch (RestClientException e) {
      Map<String, Object> fake = new LinkedHashMap<>();
      fake.put("status", "FAKE_SENT");
      fake.put("payload", payload);
      return fake;
    }
  }
}
