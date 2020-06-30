package analysis.healthfood.controller.dto;

import groovy.transform.builder.Builder;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.util.Arrays;
import java.util.List;


@Data @NoArgsConstructor
@Getter
public class ProductTotalInfoDto {

    private String productName;

    private String dailyDose;

    private String storageCaution;

    private String warningInfo;

    private String functionContent;

    private String standardInfo;

    private List<String> materialsInfo;

    private String category;

    private String materialWarningInfo;

    @Builder
    public ProductTotalInfoDto(final String productName, final String dailyDose, final String storageCaution,
                               final String warningInfo, final String functionContent, final String standardInfo,
                               final String materialsInfo, final String category, final String materialWarningInfo) {
        this.productName = productName;
        this.dailyDose = dailyDose;
        this.storageCaution = storageCaution;
        this.warningInfo = warningInfo;
        this.functionContent = functionContent;
        this.standardInfo = standardInfo;
        this.materialsInfo = Arrays.asList(materialsInfo.split("\\|"));
        this.category = category;
        this.materialWarningInfo = materialWarningInfo;
    }
}
