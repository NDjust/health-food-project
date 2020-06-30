package analysis.healthfood.controller;

import analysis.healthfood.controller.dto.MaterialWarningCountDto;
import analysis.healthfood.domain.FunctionalProduct;
import analysis.healthfood.domain.ProductTotalInfo;
import analysis.healthfood.service.ProductTotalInfoService;
import com.google.gson.Gson;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.*;

import java.util.*;
import java.util.stream.Collectors;

@Controller
@RequiredArgsConstructor
public class ProductInfoController {

    private final ProductTotalInfoService productTotalInfoService;

    @GetMapping("/product/{productName}")
    public String getProductInfo(@PathVariable("productName") final String productName,
                                 Model model) {
        ProductTotalInfo productInfoByName = productTotalInfoService.getProductInfoByName(productName);
        Map<String, String> warningMaterialInfo = getMaterialInfoMap(productInfoByName.getMaterialWarningInfo());

        model.addAttribute("productInfo", productInfoByName);
        model.addAttribute("materials", new HashSet<>(Arrays.asList(productInfoByName.getMaterialsInfo().split("\\|"))));
        model.addAttribute("warningMaterialMap", warningMaterialInfo);
        model.addAttribute("warningMaterials", warningMaterialInfo.keySet());

        return "product/product_info";
    }

    @PostMapping("/search")
    public void searchProduct(@RequestParam(value = "search") final String search,
                                 Model model) {
//        model.addAttribute("search", search);
        getProductInfo(search, model);
    }

    @GetMapping("/search")
    public String searchProductPage() {
        return "product/search";
    }

    @GetMapping("/product/materialChart/{productName}")
    public @ResponseBody String materialChart(@PathVariable("productName") final String productName){
        Gson goson = new Gson();

        System.out.println(productName);
        ProductTotalInfo productTotalInfo = productTotalInfoService.getProductInfoByName(productName);
        System.out.println(productTotalInfo);
        Map<String, String> materialInfoMap = getMaterialInfoMap(productTotalInfo.getMaterialWarningInfo());
        List<String> materials = Arrays.asList(productTotalInfo.getMaterialsInfo().split("\\|"));
        List<String> warningMaterialNames = new ArrayList<>(materialInfoMap.keySet());
        materials.removeAll(warningMaterialNames);

        for (String material : materials) {
            for (String warningMaterialName : warningMaterialNames) {
                if (material.contains(warningMaterialName)) {
                    materials.remove(material);
                }
            }
        }
        HashSet<String> notWarningMaterials = new HashSet<>(materials);
        List<MaterialWarningCountDto> warningCountDtos = new ArrayList<>();
        warningCountDtos.add(new MaterialWarningCountDto("Warning", warningMaterialNames.size()));
        warningCountDtos.add(new MaterialWarningCountDto("Safe", notWarningMaterials.size()));

        return goson.toJson(warningCountDtos);
    }
    private Map<String, String> getMaterialInfoMap(String materialWarningInfo) {
        String substring = materialWarningInfo.substring(1, materialWarningInfo.length() - 2);
        String[] split = substring.split("]");

        Map<String, String> materialInfoMap = new LinkedHashMap<>();
        for (String s : split) {
            String[] split1 = s.substring(1,s.length()).split(",");
            String materialName = split1[0].replace("[", "");
            String warningInfo = split1[1].replace("[", "");
            materialInfoMap.put(materialName, warningInfo);
            System.out.println(String.format("materialName : %s  , warningInfo : %s", materialName, warningInfo));
        }

        System.out.println(materialWarningInfo);

        return materialInfoMap;
    }
}
