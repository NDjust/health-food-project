package analysis.healthfood.repository;

import analysis.healthfood.domain.FunctionalProduct;
import org.springframework.data.jpa.repository.JpaRepository;

public interface FunctionalProductRepository extends JpaRepository<FunctionalProduct, Long> {
}
