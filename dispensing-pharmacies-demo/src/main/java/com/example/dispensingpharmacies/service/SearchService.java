package com.example.dispensingpharmacies.service;

import com.example.dispensingpharmacies.adaptor.BenefitAdaptor;
import com.example.dispensingpharmacies.adaptor.InventoryAdaptor;
import com.example.dispensingpharmacies.adaptor.MemberAdaptor;
import com.example.dispensingpharmacies.adaptor.NotificationAdaptor;
import com.example.dispensingpharmacies.adaptor.PharmacyAdaptor;
import com.example.dispensingpharmacies.model.MemberResponse;
import com.example.dispensingpharmacies.model.PharmacyResponse;
import com.example.dispensingpharmacies.model.SearchRequest;
import com.example.dispensingpharmacies.rule.DoDOverrideRule;
import com.example.dispensingpharmacies.rule.GACRule;
import com.example.dispensingpharmacies.rule.QOHRule;
import java.util.LinkedHashMap;
import java.util.Map;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class SearchService {

  private final MemberAdaptor memberAdaptor;
  private final PharmacyAdaptor pharmacyAdaptor;
  private final BenefitAdaptor benefitAdaptor;
  private final InventoryAdaptor inventoryAdaptor;
  private final NotificationAdaptor notificationAdaptor;
  private final DoDOverrideRule doDOverrideRule;
  private final GACRule gacRule;
  private final QOHRule qohRule;

  public Map<String, Object> search(SearchRequest request) {
    String memberId = request.getMemberId();
    String npi = request.getNpi();

    MemberResponse member = memberAdaptor.fetchEligibility(memberId);
    PharmacyResponse pharmacy = npi != null ? pharmacyAdaptor.fetchPharmacy(npi) : null;
    Map<String, Object> benefits =
        memberId != null ? benefitAdaptor.fetchBenefits(memberId) : Map.of();
    Map<String, Object> stock =
        npi != null ? inventoryAdaptor.fetchStock(npi, request.getQuantity()) : Map.of();

    boolean dodOk = doDOverrideRule.passes(request);
    boolean gacOk = gacRule.passes(request);
    boolean qohOk = qohRule.passes(stock);

    Map<String, Object> rules = new LinkedHashMap<>();
    rules.put("doDOverrideRule", dodOk);
    rules.put("gacRule", gacOk);
    rules.put("qohRule", qohOk);

    Map<String, Object> notifyPayload = new LinkedHashMap<>();
    notifyPayload.put("memberId", memberId);
    notifyPayload.put("npi", npi);
    notifyPayload.put("event", "SEARCH_COMPLETED");
    Map<String, Object> notification = notificationAdaptor.sendNotification(notifyPayload);

    Map<String, Object> out = new LinkedHashMap<>();
    out.put("member", member);
    out.put("pharmacy", pharmacy);
    out.put("benefits", benefits);
    out.put("inventory", stock);
    out.put("rules", rules);
    out.put("allRulesPassed", dodOk && gacOk && qohOk);
    out.put("notification", notification);
    return out;
  }
}
