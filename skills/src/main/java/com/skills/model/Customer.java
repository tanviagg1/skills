package com.skills.model;

public record Customer(
        String cardNumber,
        String fullName,
        String email,
        String phone,
        String address,
        String accountStatus,
        String creditLimit,
        String currentBalance
) {}
