package com.example.springDemo.config;

import com.example.springDemo.domain.Account;
import com.example.springDemo.writer.AccountJdbcItemWriter;
import com.example.springDemo.reader.CsvInterestReader;
import com.example.springDemo.processor.InterestCalculator;
import org.springframework.batch.core.Job;
import org.springframework.batch.core.Step;
import org.springframework.batch.core.job.builder.JobBuilder;
import org.springframework.batch.core.repository.JobRepository;
import org.springframework.batch.core.step.builder.StepBuilder;
import org.springframework.batch.item.ItemReader;
import org.springframework.batch.item.ItemWriter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.transaction.PlatformTransactionManager;

import javax.sql.DataSource;

@Configuration
public class BatchConfiguration {
    @Autowired
    private DataSource dataSource;

    @Bean
    public Job calculateInterestJob(JobRepository jobRepository, Step calculateInterestStep) {
        return new JobBuilder("CalculateInterestJob", jobRepository)
                .start(calculateInterestStep)
                .build();
    }

    @Bean
    public Step calculateInterestStep(JobRepository jobRepository, PlatformTransactionManager transactionManager,
                                      ItemReader<Account> interestItemReader,
                                      InterestCalculator interestCalculator,
                                      ItemWriter<Account> accountItemWriter) {
        return new StepBuilder("CalculateInterestStep", jobRepository)
                .<Account, Account> chunk(10, transactionManager)
                .reader(interestItemReader)
                .processor(interestCalculator)
                .writer(accountItemWriter)
                .allowStartIfComplete(true)
                .build();
    }

    @Bean
    public ItemReader<Account> itemReader() {
        return new CsvInterestReader();
    }

    @Bean
    public InterestCalculator itemProcessor() {
        return new InterestCalculator(dataSource);
    }

    @Bean
    public ItemWriter<Account> itemWriter() {
        return new AccountJdbcItemWriter(dataSource);
    }
}
