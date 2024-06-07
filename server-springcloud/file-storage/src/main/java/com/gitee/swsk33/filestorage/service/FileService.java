package com.gitee.swsk33.filestorage.service;

import com.gitee.swsk33.entity.model.Result;
import io.github.swsk33.fileliftcore.model.BinaryContent;
import io.github.swsk33.fileliftcore.model.file.MinioFile;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

/**
 * 分布式文件系统的操作服务
 */
@Service
public interface FileService {

	/**
	 * 上传文件
	 *
	 * @param file 上传的文件对象
	 * @return 结果对象，包含文件的id
	 */
	Result<String> uploadFile(MultipartFile file);

	/**
	 * 删除文件
	 *
	 * @param id 文件id
	 * @return 删除结果
	 */
	Result<Void> deleteFile(String id);

	/**
	 * 获取文件元数据信息
	 *
	 * @param id 文件id
	 * @return 得到的文件元数据
	 */
	Result<MinioFile> getFileData(String id);

	/**
	 * 下载文件
	 *
	 * @param id 文件id
	 * @return 文件的二进制信息
	 */
	Result<BinaryContent> downloadFile(String id);

}