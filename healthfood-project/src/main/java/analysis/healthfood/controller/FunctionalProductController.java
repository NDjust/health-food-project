package analysis.healthfood.controller;

import analysis.healthfood.domain.FunctionalProduct;
import analysis.healthfood.domain.ProductTotalInfo;
import analysis.healthfood.service.FunctionalProductService;
import analysis.healthfood.service.ProductTotalInfoService;
import com.google.gson.Gson;
import lombok.RequiredArgsConstructor;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.*;
import java.util.stream.Collectors;

@Controller
@RequiredArgsConstructor
public class FunctionalProductController {

    private final ProductTotalInfoService infoService;

    private final FunctionalProductService functionalProductService;

    @GetMapping(value = "/category_products")
    public String productCategoryList(Model model) {
        List<ProductTotalInfo> categoryProducts = infoService.getCategoryProducts("장");

        model.addAttribute("category_products", categoryProducts);
        return "category/list";
    }

    @GetMapping(value = "/category")
    public String categoryPage(Model model) {
        List<FunctionalProduct> allCategory = functionalProductService.getAllCategory();

        model.addAttribute("category", allCategory);
        return "category/category_list";
    }

    @GetMapping(value="category/chart")
    public @ResponseBody String categoryChart(ModelMap modelMap){
        Gson goson = new Gson();

        List<FunctionalProduct> allCategory = functionalProductService.getAllCategory();
        return goson.toJson(allCategory);
    }

    @GetMapping(value = "/category/{categoryId}")
    public String categoryPage(Model model,
                               @PathVariable("categoryId") Long categoryId) {
        FunctionalProduct functionalProduct = functionalProductService.findOneById(categoryId);
        List<String> products = Arrays.stream(functionalProduct.getProducts().split("\\|"))
                .collect(Collectors.toList());
        model.addAttribute("categoryProduct", products);
        return "category/category_detail";
    }
}
