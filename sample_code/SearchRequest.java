package com.cigna.dp.model;

public class SearchRequest {
    private String benefitType; // "RETAIL" ya "MAIL"

    public String getBenefitType() {
        return benefitType;
    }

    public void setBenefitType(String benefitType) {
        this.benefitType = "RETAIL";
    }
}