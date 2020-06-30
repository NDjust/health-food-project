package analysis.healthfood.service;

import analysis.healthfood.domain.ProductTotalInfo;
import analysis.healthfood.domain.RegistrationInfo;
import analysis.healthfood.repository.ProductTotalInfoRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class ProductTotalInfoService {

    private final ProductTotalInfoRepository infoRepository;

    public List<ProductTotalInfo> getCategoryProducts(final String category) {
        List<ProductTotalInfo> allByCategory = infoRepository.findAllByCategory(category);

        return allByCategory;
    }

    public ProductTotalInfo getProductInfoByName(final String productName) {
        return infoRepository.findByName(productName);
    }

    public List<ProductTotalInfo> getAll() {
        return infoRepository.findAll();
    }
}
