package analysis.healthfood.service;

import analysis.healthfood.domain.RegistrationInfo;
import analysis.healthfood.repository.RegistrationInfoRepository;
import groovy.util.logging.Slf4j;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Slf4j
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class RegistrationInfoService {

    private final RegistrationInfoRepository registrationInfoRepository;

    public List<RegistrationInfo> getAllRegisterInfo() {
        try {
            return registrationInfoRepository.findAllRegisterInfo();
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
}

