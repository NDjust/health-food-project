package analysis.healthfood.domain;

import lombok.Data;
import lombok.Getter;
import lombok.NoArgsConstructor;

import javax.persistence.Entity;
import javax.persistence.Id;

@Entity
@NoArgsConstructor @Getter
public class ProductTotalInfo {

    @Id
    private Long productInfoId;

    private String companyName;

    private String productName;

    private long reportNum;

    private String registerDate;

    private String expiryDate;

    private String properties;

    private String dailyDose;

    private String packageType;

    private String storageCaution;

    private String warningInfo;

    private String functionContent;

    private String standardInfo;

    private String materialsInfo;

    private String category;

    private String materialWarningInfo;

}
