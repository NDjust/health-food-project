package analysis.healthfood.domain;

import lombok.NoArgsConstructor;

import javax.persistence.Entity;
import javax.persistence.Id;

@Entity
@NoArgsConstructor
public class ProductInfo {

    @Id
    private Long productInfoId;

    private String companyName;

    private String reportNum;

    private String registerDate;

    private String expiryDate;

    private String properties;

    private String dailyDose;

    private String packageType;

    private String storageCaution;

    private String warningInfo;

    private String functionContent;

//    private String
}
