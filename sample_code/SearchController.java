package com.cigna.dp.controller;

import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;

@RestController
@RequestMapping("/dispensingPharmacies")
public class SearchController {
    
    private final SearchService searchService;

    public SearchController(SearchService searchService) {
        this.searchService = searchService;
    }

    @PostMapping("/search")
    public ResponseEntity<String> search(@RequestBody SearchRequest request) {
        String optimalPharmacy = searchService.findOptimalPharmacy(request);
        return ResponseEntity.ok(optimalPharmacy);
    }
}