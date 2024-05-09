package com.example.springDemo.processor;

import com.example.springDemo.domain.Account;
import org.springframework.batch.item.ItemProcessor;

import javax.sql.DataSource;
import java.math.BigDecimal;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class InterestCalculator implements ItemProcessor<Account, Account> {

    private final DataSource dataSource;

    public InterestCalculator(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    @Override
    public Account process(Account account) throws Exception {
        BigDecimal balance = fetchBalanceFromDB2(account.getAccountNumber(), dataSource);
        if (balance != null) {
            BigDecimal interest = balance.multiply(account.getInterest());

            //Update account with interest rate
            account.setBalance(balance.add(interest));
        }
        return account;
    }

    private BigDecimal fetchBalanceFromDB2(String account_number, DataSource dataSource) {
        String sql = "SELECT balance FROM account WHERE account_number = ?";
        try (Connection connection = dataSource.getConnection();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setString(1, account_number);
            try (ResultSet resultSet = statement.executeQuery()) {
                if (resultSet.next()) {
                    return resultSet.getBigDecimal("balance");
                }
            }
        } catch (Exception e) {
            // Handle any exceptions that may occur during database access
            e.printStackTrace(); // Replace with proper error handling
        }
        return null; // Return null if balance is not found or any error occurs
    }
}

