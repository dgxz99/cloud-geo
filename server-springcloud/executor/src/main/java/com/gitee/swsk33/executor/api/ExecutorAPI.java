package com.gitee.swsk33.executor.api;

import cn.zhxu.okhttps.HTTP;
import cn.zhxu.okhttps.HttpResult;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/executor")
public class ExecutorAPI {

	@Autowired
	private HTTP httpClient;

	@PostMapping(value = "/{service}")
	public ResponseEntity<String> getResult(@RequestBody String body, @PathVariable String service) {
		HttpResult result = httpClient.sync("/" + service).setBodyPara(body).bodyType("json").post();
		if (result.isSuccessful()) {
			return ResponseEntity.ok().contentType(MediaType.APPLICATION_JSON).body(result.getBody().toString());
		} else {
			return ResponseEntity.internalServerError().contentType(MediaType.APPLICATION_JSON).body(result.getBody().toString());
		}
	}

}