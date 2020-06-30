package analysis.healthfood.domain;

import lombok.Getter;
import lombok.NoArgsConstructor;

import javax.persistence.Entity;
import javax.persistence.Id;

@Entity @Getter
@NoArgsConstructor
public class FunctionalProduct {

    @Id
    private Long id;

    private String category;

    private String ingredients;

    private String products;

    private String productCount;

}
