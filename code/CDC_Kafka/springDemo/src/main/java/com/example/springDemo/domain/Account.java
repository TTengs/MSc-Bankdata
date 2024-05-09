package com.example.springDemo.domain;

import lombok.Getter;
import lombok.Setter;

import java.math.BigDecimal;

@Getter @Setter
public class Account {
    private Long id;
    private String accountNumber;
    private String accountHolderFirstName;
    private String accountHolderLastName;
    private BigDecimal balance;
}
