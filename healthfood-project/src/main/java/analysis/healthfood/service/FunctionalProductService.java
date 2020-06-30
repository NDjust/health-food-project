package analysis.healthfood.service;

import analysis.healthfood.domain.FunctionalProduct;
import analysis.healthfood.repository.FunctionalProductRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class FunctionalProductService {

    private final FunctionalProductRepository functionalProductRepository;


    public List<FunctionalProduct> getAllCategory() {
        return functionalProductRepository.findAll();
    }

    public FunctionalProduct findOneById(final Long categoryId) {
        return functionalProductRepository.findById(categoryId)
                .orElse(null);
    }
}
