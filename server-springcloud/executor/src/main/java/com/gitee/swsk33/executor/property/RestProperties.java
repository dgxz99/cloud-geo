package com.gitee.swsk33.executor.property;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Data
@Component
@ConfigurationProperties(prefix = "com.gitee.swsk33.executor")
public class RestProperties {

	/**
	 * pyWPS的地址
	 */
	private String host = "127.0.0.1";

	/**
	 * pyWPS端口
	 */
	private int port = 5000;

	/**
	 * pyWPS前置路径
	 */
	private String basePath = "/";

}