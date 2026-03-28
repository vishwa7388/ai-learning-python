package com.example.dispensingpharmacies.controller;

import com.example.dispensingpharmacies.model.SearchRequest;
import com.example.dispensingpharmacies.service.SearchService;
import java.util.Map;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/search")
@RequiredArgsConstructor
public class SearchController {

  private final SearchService searchService;

  @PostMapping
  public ResponseEntity<Map<String, Object>> search(@RequestBody SearchRequest request) {
    return ResponseEntity.ok(searchService.search(request));
  }
}
