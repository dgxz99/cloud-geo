package com.gitee.swsk33.executor;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

@EnableDiscoveryClient
@SpringBootApplication
public class ExecutorApplication {

	public static void main(String[] args) {
		SpringApplication.run(ExecutorApplication.class, args);
	}

}