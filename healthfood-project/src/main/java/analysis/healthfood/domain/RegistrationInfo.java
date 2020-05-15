package analysis.healthfood.domain;

import lombok.Getter;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;

@Entity
@Getter
public class RegistrationInfo {

    @Id
    @Column(name = "register_no")
    @GeneratedValue
    private Long registerNo;

    @Column(name = "product_search_no")
    private Long productSearchNo;

    @Column(name = "report_num")
    private Long reportNum;

    @Column(name = "product_name")
    private String productName;

    @Column(name = "company_name")
    private String companyName;

    @Column(name = "register_date")
    private String registerDate;

}