package com.example.springDemo.reader;

import com.example.springDemo.domain.Account;
import org.springframework.batch.item.ExecutionContext;
import org.springframework.batch.item.ItemReader;
import org.springframework.batch.item.file.FlatFileItemReader;
import org.springframework.batch.item.file.mapping.BeanWrapperFieldSetMapper;
import org.springframework.batch.item.file.mapping.DefaultLineMapper;
import org.springframework.batch.item.file.transform.DelimitedLineTokenizer;
import org.springframework.core.io.ClassPathResource;

public class CsvAccountReader implements ItemReader<Account> {
    private final FlatFileItemReader<Account> reader;

    public CsvAccountReader() {
        this.reader = new FlatFileItemReader<>();
        this.reader.setResource(new ClassPathResource("data.csv"));

        DelimitedLineTokenizer tokenizer = new DelimitedLineTokenizer();
        tokenizer.setNames(new String[]{"accountNumber", "accountHolderFirstName", "accountHolderLastName", "balance"});
        tokenizer.setDelimiter(",");

        BeanWrapperFieldSetMapper<Account> fieldSetMapper = new BeanWrapperFieldSetMapper<>();
        fieldSetMapper.setTargetType(Account.class);

        DefaultLineMapper<Account> lineMapper = new DefaultLineMapper<>();
        lineMapper.setLineTokenizer(tokenizer);
        lineMapper.setFieldSetMapper(fieldSetMapper);

        this.reader.setLineMapper(lineMapper);

        //Skip header line
        this.reader.setLinesToSkip(1);

        this.reader.open(new ExecutionContext());
    }

    @Override
    public Account read() throws Exception {
        return reader.read();
    }
}
