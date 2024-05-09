package com.example.springDemo.processor;

import com.example.springDemo.domain.Account;
import org.springframework.batch.item.ItemProcessor;

import java.math.BigDecimal;

public class InterestCalculator implements ItemProcessor<Account, Account> {

    private final BigDecimal interestRate;

    public InterestCalculator(BigDecimal interestRate) {
        this.interestRate = interestRate;
    }

    @Override
    public Account process(Account account) throws Exception {
        BigDecimal interest = account.getBalance().multiply(interestRate);

        //Update account with interest rate
        account.setBalance(account.getBalance().add(interest));
        return account;
    }
}
