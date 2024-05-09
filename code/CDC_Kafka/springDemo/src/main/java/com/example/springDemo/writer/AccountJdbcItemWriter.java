package com.example.springDemo.writer;

import com.example.springDemo.domain.Account;
import org.springframework.batch.item.database.JdbcBatchItemWriter;

import javax.sql.DataSource;

public class AccountJdbcItemWriter extends JdbcBatchItemWriter<Account> {

    public AccountJdbcItemWriter(DataSource dataSource) {
        setDataSource(dataSource);
        setSql("INSERT INTO account (account_number, account_holder_first_name, account_holder_last_name, balance) VALUES (?, ?, ?, ?)");
        setItemPreparedStatementSetter((account, preparedStatement) -> {
            //Print account data instead of setting it in prepared statement
            preparedStatement.setString(1, account.getAccountNumber());
            preparedStatement.setString(2, account.getAccountHolderFirstName());
            preparedStatement.setString(3, account.getAccountHolderLastName());
            preparedStatement.setBigDecimal(4, account.getBalance());
        });
    }
}
