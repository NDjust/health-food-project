package analysis.healthfood.repository;

import analysis.healthfood.domain.ProductTotalInfo;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ProductTotalInfoRepository extends JpaRepository<ProductTotalInfo, Long> {

    @Query("select p from ProductTotalInfo p where p.category LIKE CONCAT('%', :category, '%') ")
    List<ProductTotalInfo> findAllByCategory(@Param("category") String category);

    @Query("select p from ProductTotalInfo p where p.productName = :productName")
    ProductTotalInfo findByName(@Param(("productName")) String productName);
}
