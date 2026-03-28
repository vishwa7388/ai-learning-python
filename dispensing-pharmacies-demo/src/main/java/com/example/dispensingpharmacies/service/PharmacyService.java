package com.example.dispensingpharmacies.service;

import com.example.dispensingpharmacies.adaptor.PharmacyAdaptor;
import com.example.dispensingpharmacies.model.PharmacyResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class PharmacyService {

  private final PharmacyAdaptor pharmacyAdaptor;

  public PharmacyResponse getByNpi(String npi) {
    return pharmacyAdaptor.fetchPharmacy(npi);
  }
}
