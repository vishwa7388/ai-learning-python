@RestController
@RequestMapping("/dispensingPharmacies")
public class SearchController {

    @Autowired
    private SearchService searchService;

    @PostMapping("/search")
    public ResponseEntity<SearchResponse> search(
            @RequestBody SearchRequest request) {
        return ResponseEntity.ok(searchService.findOptimalPharmacy(request));
    }
}

@Service
public class SearchService {

    @Autowired
    private DrugAdaptor drugAdaptor;
    @Autowired
    private MembershipAdaptor membershipAdaptor;
    @Autowired
    private RxRoutingAdaptor rxRoutingAdaptor;

    public SearchResponse findOptimalPharmacy(SearchRequest request) {
        DrugInfo drug = drugAdaptor.getDrugInfo(request.getNdc());
        MemberInfo member = membershipAdaptor.getMemberInfo(request.getPatientId());
        List<Pharmacy> pharmacies = rxRoutingAdaptor.getRouting(drug, member);
        return applyBusinessRules(pharmacies, member);
    }

    private SearchResponse applyBusinessRules(List<Pharmacy> pharmacies, MemberInfo member) {
        // Apply GAC Rule, QOH Rule, DoD Override
        return new SearchResponse(pharmacies.get(0), pharmacies.subList(1, pharmacies.size()));
    }
}