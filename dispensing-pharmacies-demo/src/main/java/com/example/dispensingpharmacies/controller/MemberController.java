package com.example.dispensingpharmacies.controller;

import com.example.dispensingpharmacies.adaptor.MemberAdaptor;
import com.example.dispensingpharmacies.model.MemberResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/member")
@RequiredArgsConstructor
public class MemberController {

  private final MemberAdaptor memberAdaptor;

  @GetMapping("/{memberId}/eligibility")
  public ResponseEntity<MemberResponse> eligibility(@PathVariable String memberId) {
    return ResponseEntity.ok(memberAdaptor.fetchEligibility(memberId));
  }
}
