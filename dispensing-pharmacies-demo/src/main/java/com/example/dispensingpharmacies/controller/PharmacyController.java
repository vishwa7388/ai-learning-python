package com.example.dispensingpharmacies.controller;

import com.example.dispensingpharmacies.model.PharmacyResponse;
import com.example.dispensingpharmacies.service.PharmacyService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/pharmacy")
@RequiredArgsConstructor
public class PharmacyController {

  private final PharmacyService pharmacyService;

  @GetMapping("/{npi}")
  public ResponseEntity<PharmacyResponse> getPharmacy(@PathVariable String npi) {
    return ResponseEntity.ok(pharmacyService.getByNpi(npi));
  }
}
