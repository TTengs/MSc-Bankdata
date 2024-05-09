package com.example.springDemo.writer;

import com.example.springDemo.domain.Account;
import org.springframework.batch.item.database.JdbcBatchItemWriter;

import javax.sql.DataSource;

public class AccountJdbcItemWriter extends JdbcBatchItemWriter<Account> {

    public AccountJdbcItemWriter(DataSource dataSource) {
        setDataSource(dataSource);
        setSql("UPDATE account SET balance = ? WHERE account_number = ?");
        setItemPreparedStatementSetter((account, preparedStatement) -> {
            preparedStatement.setBigDecimal(1, account.getBalance());
            preparedStatement.setString(2, account.getAccountNumber());
        });
    }
}
