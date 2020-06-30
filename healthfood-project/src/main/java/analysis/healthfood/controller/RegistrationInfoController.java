package analysis.healthfood.controller;

import analysis.healthfood.domain.ProductTotalInfo;
import analysis.healthfood.service.ProductTotalInfoService;
import analysis.healthfood.service.RegistrationInfoService;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.List;

@Controller
@RequiredArgsConstructor
public class RegistrationInfoController {
    private final RegistrationInfoService registrationInfoService;
    private final ProductTotalInfoService productTotalInfoService;

    @GetMapping(value = "/register_info")
    public String registerInfoList(Model model) {
        List<ProductTotalInfo> allRegistrationInfo = productTotalInfoService.getAll();

        model.addAttribute("productInfo", allRegistrationInfo);
        return "product/register";
    }

    @Data
    @AllArgsConstructor
    private static class Result<T> {
        private int counts;
        private T data;
    }
}
