package com.gitee.swsk33.executor.config;

import cn.hutool.core.util.StrUtil;
import cn.zhxu.okhttps.HTTP;
import com.gitee.swsk33.executor.property.RestProperties;
import okhttp3.OkHttpClient;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.concurrent.TimeUnit;

@Configuration
public class HTTPClientConfig {

	@Bean
	public HTTP httpClient(RestProperties restProperties) {
		String baseURL = String.format("http://%s:%d%s", restProperties.getHost(), restProperties.getPort(), StrUtil.isEmpty(restProperties.getBasePath()) ? "" : restProperties.getBasePath());
		return HTTP.builder().config((OkHttpClient.Builder builder) -> {
			builder.connectTimeout(1, TimeUnit.HOURS);
			builder.writeTimeout(1, TimeUnit.HOURS);
			builder.readTimeout(1, TimeUnit.HOURS);
		}).baseUrl(baseURL).build();
	}

}