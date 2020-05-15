package analysis.healthfood.controller;

import analysis.healthfood.domain.RegistrationInfo;
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


    @GetMapping(value = "/register_info")
    public String registerInfoList(Model model) {
        List<RegistrationInfo> allRegistrationInfo = registrationInfoService.getAllRegisterInfo();
        model.addAttribute("register_info", allRegistrationInfo);
        return "register-info/register";
    }

    @Data
    @AllArgsConstructor
    private static class Result<T> {
        private int counts;
        private T data;
    }
}
