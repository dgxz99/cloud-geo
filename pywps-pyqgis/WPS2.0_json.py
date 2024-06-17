WPS2_description_json = {
	"Title": "",  # 算子标题
	"Abstract": "",  # 算子功能简短描述
	"Identifier": "",  # 算子唯一标识符
	"keywords": [],  # 描述算子的关键字
	"Metadata": [],  # 其他描述信息，一般以简单链接的方式存储；如：{"title": "","href": "","role": "","type": ""}
	"Input": [  # 算子的输入参数
		{
			"Title": "",
			"Abstract": "",
			"Identifier": "",
			"keywords": [],
			"Metadata": [],
			"minOccurs": "",  # 该参数最小出现次数，默认为1
			"maxOccurs": "",  # 该参数最大出现次数，默认为1
			"DataType": "ComplexData",  # 该参数数据类型：ComplexData、LiteralData、BoundingBoxData
			"ComplexData": {
				"Format": [  # 支持的所有数据格式
					{
						"mimeType": "",
						"encoding": "",
						"schema": "",
						"maximumMegabytes": "",  # 输入数据的最大大小，单位：M 可选参数
						"default": ""  # 该参数默认数据类型，不设置该参数默认为false，但所有数据格式中必须设置一种为默认
					}
				]
			}
		},
		{
			"Title": "",
			"Abstract": "",
			"Identifier": "",
			"keywords": [],
			"Metadata": [],
			"minOccurs": "",  # 该参数最小出现次数，默认为1
			"maxOccurs": "",  # 该参数最大出现次数，默认为1
			"DataType": "LiteralData",  # 该参数数据类型：ComplexData、LiteralData、BoundingBoxData
			"LiteralData": {
				"Format": [],
				"LiteralDataDomain": [
					{
						"AllowedValues": {},  # AllowedValues（list|range）、AnyValue、ValuesReference三选一
						"DataType": {
							"reference": "http://www.w3.org/2001/XMLSchema#{content}",  # content取下面的值
							"content": ""  # 数据类型：String、Integer、Decimal、Boolean、Double、Float
						},
						"UOM": "",  # 单位，可选
						"DefaultValue": "",  # 默认值，可选
						"default": "",
					}
				]
			}
		},
		{
			"Title": "",
			"Abstract": "",
			"Identifier": "",
			"keywords": [],
			"Metadata": [],
			"minOccurs": "",  # 该参数最小出现次数，默认为1
			"maxOccurs": "",  # 该参数最大出现次数，默认为1
			"DataType": "BoundingBoxData",  # 该参数数据类型：ComplexData、LiteralData、BoundingBoxData
			"BoundingBoxData": {
				"Format": [],
				"SupportedCRS": [
					{
						"CRS": "URI",
						"default": ""
					}
				]
			}
		},
	],
	"Output": []  # 同Input
}

status_info = {
	"JobID": "",
	"Status": "",  # 完成状态 Succeeded Failed Accepted Running
	"ExpirationDate": "",  # 该任务失效时间（即删除该任务记录时间）
	"EstimatedCompletion": "",  # 算子运行结束时间
	"NextPoll": "",  # 下一次轮询时间
	"PercentCompleted": ""  # 完成进度
}

result = {
	"JobID": "",
	"ExpirationDate": "",  # 该任务失效时间（即删除该任务记录时间）
	"Output": {

	}
}

# table 29
ProcessOfferingProperties = {
	"jobControlOptions": ["sync-execute", "async-execute"],  # 任务执行的类型
	"outputTransmission": ["value", "reference"],  # 支持传输的类型
	"processVersion": "",
	"processModel": ""  # Type of the process description. Defaults to “native”.
}

getCapabilitiesResponse = {
	"service": "WPS",
	"version": "2.0",
	"title": "",
	"abstract": "",
	"keywords": [],
	"keywords_type": [],
	"provider": {},
	"contents": [{  # processSummary
		"Title": "",
		"Abstract": "",
		"Identifier": "",
		# "processModel": "native",
		# "jobControlOptions": ["sync-execute", "async-execute"],
		# "outputTransmission": ["value", "reference"]
	}]
}

describeProcessResponse = {
	"process": {},  # 算子wps2.0规范的信息
	# "processModel": "native",
	"jobControlOptions": ["sync-execute", "async-execute"],
	"outputTransmission": ["value", "reference"]
}

executeResponse = {
	"JobID": "",
	"ExpirationDate": "",  # 该任务失效时间（即删除该任务记录时间）
	"Status": "",
	"EstimatedCompletion": "",  # 算子运行结束时间
	"PercentCompleted": "",  # 完成进度
	"Message": "",
	"Output": {}
}

asyncExecuteResponse = {
	"JobID": "",
	"Status": "",  # 完成状态 Succeeded Failed Accepted Running
	"Result": {
		"ExpirationDate": "",  # 该任务失效时间（即删除该任务记录时间）
		"EstimatedCompletion": "",  # 算子运行结束时间
		"PercentCompleted": "",  # 完成进度
		"Message": "",
		"Output": {}
	}
}
