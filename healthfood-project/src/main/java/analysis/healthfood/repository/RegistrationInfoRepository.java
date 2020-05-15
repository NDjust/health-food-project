package analysis.healthfood.repository;

import analysis.healthfood.domain.RegistrationInfo;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Repository;

import javax.persistence.EntityManager;
import java.util.List;

@Repository
@RequiredArgsConstructor
public class RegistrationInfoRepository {

    private final EntityManager em;

    public List<RegistrationInfo> findAllRegisterInfo() {
        return em.createQuery("select m from RegistrationInfo m").getResultList();
    }
}
