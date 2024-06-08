package com.gitee.swsk33.filestorage.api;

import com.gitee.swsk33.entity.model.Result;
import com.gitee.swsk33.filestorage.service.FileService;
import io.github.swsk33.fileliftcore.model.BinaryContent;
import io.github.swsk33.fileliftcore.model.file.MinioFile;
import io.github.swsk33.fileliftcore.model.file.UploadFile;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ContentDisposition;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

/**
 * 文件服务API
 */
@RestController
@RequestMapping("/api/file")
public class FileAPI {

	@Autowired
	private FileService fileService;

	@PutMapping("/upload")
	public Result<UploadFile> upload(@RequestParam MultipartFile file) {
		return fileService.uploadFile(file);
	}

	@DeleteMapping("/delete/{id}")
	public Result<Void> delete(@PathVariable String id) {
		return fileService.deleteFile(id);
	}

	@GetMapping("/find/{id}")
	public Result<MinioFile> getFile(@PathVariable String id) {
		return fileService.getFileData(id);
	}

	@GetMapping("/retrieve/{name}")
	public ResponseEntity<byte[]> download(@PathVariable String name) {
		Result<BinaryContent> result = fileService.downloadFile(name);
		if (!result.isSuccess()) {
			return ResponseEntity.notFound().build();
		}
		// 获取内容
		BinaryContent content = result.getData();
		// 设定响应头
		HttpHeaders headers = new HttpHeaders();
		// 设定MediaType类型
		headers.setContentType(MediaType.parseMediaType(content.getContentType()));
		// 设定Content-Disposition头，告诉浏览器下载的文件名称
		headers.setContentDisposition(ContentDisposition.builder("attachment").filename(name).build());
		// 返回响应
		return ResponseEntity.ok().headers(headers).body(content.getByteAndClose());
	}

}