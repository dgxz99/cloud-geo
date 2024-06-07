process_WPS2_description_json = {
	"Title": "",			# 算子标题
	"Abstract": "",			# 算子功能简短描述
	"Identifier": "",		# 算子唯一标识符
	"keywords": [],			# 描述算子的关键字
	"Metadata": [],			# 其他描述信息，一般以简单链接的方式存储；如：{"title": "","href": "","role": "","type": ""}
	"Input": [				# 算子的输入参数
		{
			"Title": "",
			"Abstract": "",
			"Identifier": "",
			"keywords": [],
			"Metadata": [],
			"minOccurs": "",				# 该参数最小出现次数，默认为1
			"maxOccurs": "",				# 该参数最大出现次数，默认为1
			"DataType": "ComplexData",		# 该参数数据类型：ComplexData、LiteralData、BoundingBoxData
			"ComplexData": {
				"Format": [					# 支持的所有数据格式
					{
						"mimeType": "",
						"encoding": "",
						"schema": "",
						"maximumMegabytes": "",	 # 输入数据的最大大小，单位：M 可选参数
						"default": ""		 	 # 该参数默认数据类型，不设置该参数默认为false，但所有数据格式中必须设置一种为默认
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
							"content": ""	  # 数据类型：String、Integer、Decimal、Boolean、Double、Float
						},
						"UOM": "",			  # 单位，可选
						"DefaultValue": "",   # 默认值，可选
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
	"Output": []			# 同Input
}
