package com.gitee.swsk33.filestorage.service;

import com.gitee.swsk33.entity.model.Result;
import io.github.swsk33.fileliftcore.model.BinaryContent;
import io.github.swsk33.fileliftcore.model.file.MinioFile;
import io.github.swsk33.fileliftcore.model.file.UploadFile;
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
	 * @return 结果对象，包含已上传文件的信息
	 */
	Result<UploadFile> uploadFile(MultipartFile file);

	/**
	 * 上传文件并指定文件名
	 * @param file 上传的文件对象
	 * @param name 指定上传后的文件名，不包括扩展名
	 * @return 结果对象，包含已上传文件的信息
	 */
	Result<UploadFile> uploadFileForceName(MultipartFile file, String name);

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
	 * @param name 文件名，需要带扩展名
	 * @return 文件的二进制信息
	 */
	Result<BinaryContent> downloadFile(String name);

}