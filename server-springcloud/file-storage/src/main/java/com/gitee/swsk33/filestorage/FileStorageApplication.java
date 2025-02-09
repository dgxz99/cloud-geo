package com.gitee.swsk33.filestorage;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

@EnableDiscoveryClient
@SpringBootApplication
public class FileStorageApplication {

	public static void main(String[] args) {
		SpringApplication.run(FileStorageApplication.class, args);
	}

}