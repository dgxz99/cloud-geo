package com.gitee.swsk33.filestorage.service.impl;

import com.gitee.swsk33.entity.model.Result;
import com.gitee.swsk33.filestorage.service.FileService;
import io.github.swsk33.fileliftcore.model.BinaryContent;
import io.github.swsk33.fileliftcore.model.file.MinioFile;
import io.github.swsk33.fileliftcore.model.file.UploadFile;
import io.github.swsk33.fileliftcore.model.result.FileResult;
import io.github.swsk33.fileliftcore.service.UploadFileService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.multipart.MultipartFile;

import java.util.HashMap;
import java.util.Map;

@Component
public class FileServiceImpl implements FileService {

	@Autowired
	private UploadFileService uploadFileService;

	@Value("${file-service.url}")
	private String fileServiceUrl;

	@Override
	public Result<Map<String, Object>> uploadFile(MultipartFile file) {
		FileResult<UploadFile> result = uploadFileService.upload(file);
		if (!result.isSuccess()) {
			return Result.resultFailed(result.getMessage());
		}
		UploadFile data = result.getData();
		// 设置文件访问URL
		Map<String, Object> resultMap = new HashMap<>();
		resultMap.put("name", data.getName());
		resultMap.put("format", data.getFormat());
		resultMap.put("length", data.getLength());
		String href = fileServiceUrl + "/retrieve/" + data.getName() + "." + data.getFormat();
		resultMap.put("href", href);
		return Result.resultSuccess("上传文件完成！", resultMap);
	}

	@Override
	public Result<UploadFile> uploadFileForceName(MultipartFile file, String name) {
		FileResult<UploadFile> result = uploadFileService.uploadForceName(file, name);
		if (!result.isSuccess()) {
			return Result.resultFailed(result.getMessage());
		}
		return Result.resultSuccess("上传文件完成！", result.getData());
	}

	@Override
	public Result<Void> deleteFile(String id) {
		uploadFileService.delete(id);
		return Result.resultSuccess("删除文件完成！");
	}

	@Override
	public Result<MinioFile> getFileData(String id) {
		FileResult<UploadFile> result = uploadFileService.findByMainName(id);
		if (!result.isSuccess()) {
			return Result.resultFailed(result.getMessage());
		}
		return Result.resultSuccess("已获取文件信息！", (MinioFile) result.getData());
	}

	@Override
	public Result<BinaryContent> downloadFile(String name) {
		FileResult<BinaryContent> result = uploadFileService.downloadFileByFullName(name);
		if (!result.isSuccess()) {
			return Result.resultFailed(result.getMessage());
		}
		return Result.resultSuccess("下载成功！", result.getData());
	}

}