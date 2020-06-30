package analysis.healthfood.controller.dto;

import lombok.Data;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Data @NoArgsConstructor
@Getter
public class MaterialWarningCountDto {

    private String warningOrNotWarning;

    private int eachCount;

    public MaterialWarningCountDto(final String warningOrNotWarning, final int eachCount) {
        this.warningOrNotWarning = warningOrNotWarning;
        this.eachCount = eachCount;
    }
}
