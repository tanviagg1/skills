package com.skills.service;

import com.skills.backend.CustomerBackendClient;
import com.skills.model.Customer;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class CustomerService {

    private final CustomerBackendClient backendClient;

    public CustomerService(CustomerBackendClient backendClient) {
        this.backendClient = backendClient;
    }

    public Optional<Customer> getCustomerByCardNumber(String cardNumber) {
        return backendClient.findByCardNumber(cardNumber);
    }
}
