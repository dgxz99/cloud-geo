package com.gitee.swsk33.filestorage.service.impl;

import com.gitee.swsk33.entity.model.Result;
import com.gitee.swsk33.filestorage.service.FileService;
import io.github.swsk33.fileliftcore.model.BinaryContent;
import io.github.swsk33.fileliftcore.model.file.MinioFile;
import io.github.swsk33.fileliftcore.model.file.UploadFile;
import io.github.swsk33.fileliftcore.model.result.FileResult;
import io.github.swsk33.fileliftcore.service.UploadFileService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.multipart.MultipartFile;

@Component
public class FileServiceImpl implements FileService {

	@Autowired
	private UploadFileService uploadFileService;

	@Override
	public Result<String> uploadFile(MultipartFile file) {
		FileResult<UploadFile> result = uploadFileService.upload(file);
		if (!result.isSuccess()) {
			return Result.resultFailed(result.getMessage());
		}
		return Result.resultSuccess("上传文件完成！", result.getData().getName());
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
	public Result<BinaryContent> downloadFile(String id) {
		FileResult<BinaryContent> result = uploadFileService.downloadFileByMainName(id);
		if (!result.isSuccess()) {
			return Result.resultFailed(result.getMessage());
		}
		return Result.resultSuccess("下载成功！", result.getData());
	}

}