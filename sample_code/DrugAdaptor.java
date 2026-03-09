@Component
public class DrugAdaptor {

    @Autowired
    private RestTemplate restTemplate;

    public DrugInfo getDrugInfo(String ndc) {
        String url = "http://drug-api/v1/drugs/" + ndc;
        ResponseEntity<DrugInfo> response = 
            restTemplate.getForEntity(url, DrugInfo.class);
        if (response.getStatusCode() != HttpStatus.OK) {
            throw new DrugNotFoundException("Drug not found for NDC: " + ndc);
        }
        return response.getBody();
    }
}