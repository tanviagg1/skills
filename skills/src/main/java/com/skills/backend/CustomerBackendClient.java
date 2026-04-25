package com.skills.backend;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.skills.model.Customer;
import org.springframework.stereotype.Component;

import java.io.InputStream;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * Client for the downstream customer backend system.
 * Mock data loaded from src/main/resources/mock-customers.json.
 * Replace with real HTTP client (e.g. RestClient) when backend is available.
 */
@Component
public class CustomerBackendClient {

    private final Map<String, Customer> mockStore;

    public CustomerBackendClient() throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        InputStream is = getClass().getResourceAsStream("/mock-customers.json");
        List<Customer> customers = mapper.readValue(is, new TypeReference<>() {});
        mockStore = customers.stream().collect(Collectors.toMap(Customer::cardNumber, c -> c));
    }

    public Optional<Customer> findByCardNumber(String cardNumber) {
        return Optional.ofNullable(mockStore.get(cardNumber));
    }
}
