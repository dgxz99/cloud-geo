<!--src/components/OperatorIdentifier-->
<template>
    
    <div class="operator-identifier" v-if="operator">
        <!-- 返回按钮 -->
        <el-button type="text" class="back-button" @click="doClear()">
            <el-icon>
                <ArrowLeft/>
            </el-icon>
            <span style="font-size: 20px;">{{ operator.Identifier }}</span>
        </el-button>
        
        <!-- 算子描述 -->
        <div class="operator-abstract">{{ operator.Abstract }}</div>
        
        <!-- 输入参数部分 -->
        <div class="input-section">
            <h3>Input Parameters</h3>
            <div v-for="input in operator.Input.filter(i => i.Identifier !== 'OUTPUT' && i.Identifier !== 'output')"
                 :key="input.Identifier" class="input-field">
                <label>
                    {{ input.Identifier }}
                    <span v-if="input.minOccurs >= 1" style="color: red;">*</span>
                </label>
                <!-- 上传文件控件 -->
                <el-upload
                    v-if="input.DataType === 'ComplexData'"
                    :ref="(ref) => registerUploadRef('upload-' + input.Identifier, ref)"
                    :data="{ identifier: input.Identifier }"
                    :accept="getSupportedFormats(input.ComplexData)"
                    class="uniform-width"
                    action="/api/upload"
                    :on-success="(response, file, fileList) => handleUploadSuccess(response, file, input.Identifier)"
                    :on-error="handleUploadError"
                >
                    <el-button class="upload-button uniform-width" type="primary">Upload File</el-button>
                </el-upload>
                
                
                <!-- 输入参数选择 -->
                <el-select
                    v-if="(input.Identifier === 'OUTPUT' || input.Identifier === 'output') && input.DataType === 'ComplexData'"
                    v-model="inputValues[input.Identifier]" placeholder="Select Output Format" class="uniform-width">
                    <el-option v-for="(format, index) in input.ComplexData.Format" :key="index" :label="format.mimeType"
                               :value="format.mimeType">
                    </el-option>
                </el-select>
                
                <!-- LiteralData 类型的输入 -->
                <el-select
                    v-else-if="input.DataType === 'LiteralData' && input.LiteralData.LiteralDataDomain[0].AllowedValues?.length"
                    v-model="inputValues[input.Identifier]" placeholder="Please Select" class="uniform-width">
                    <el-option v-for="(value, index) in input.LiteralData.LiteralDataDomain[0].AllowedValues"
                               :key="index" :label="value[Object.keys(value)[0]]" :value="Object.keys(value)[0]">
                    </el-option>
                </el-select>
                
                <el-input
                    v-else-if="input.DataType === 'LiteralData' && input.LiteralData.LiteralDataDomain[0].DataType.content === 'string'"
                    v-model="inputValues[input.Identifier]" :placeholder="input.Abstract" class="uniform-width">
                </el-input>
                
                <el-input-number
                    v-else-if="input.DataType === 'LiteralData' && ['int', 'float'].includes(input.LiteralData.LiteralDataDomain[0].DataType.content)"
                    v-model="inputValues[input.Identifier]" :placeholder="input.Abstract" :min="0"
                    class="uniform-width">
                </el-input-number>
                
                <div
                    v-else-if="input.DataType === 'LiteralData' && input.LiteralData.LiteralDataDomain[0].DataType.content === 'boolean'"
                    class="boolean-input">
                    <el-switch v-model="inputValues[input.Identifier]"
                               :active-text="input.LiteralData.LiteralDataDomain[0].TrueLabel"
                               :inactive-text="input.LiteralData.LiteralDataDomain[0].FalseLabel" :active-value="true"
                               :inactive-value="false">
                    </el-switch>
                    <span class="bool-description">{{ input.Abstract }}</span>
                </div>
            </div>
            <!-- 执行模式选择 -->
            <h3>Execution Mode</h3>
            <el-radio-group v-model="mode" class="uniform-width">
                <el-radio label="sync">Synchronous</el-radio>
                <el-radio label="async">Asynchronous</el-radio>
            </el-radio-group>
        </div>
        
        <!-- 输出参数部分 -->
        <div class="output-section">
            <h3>Output Parameters</h3>
            <div v-for="output in operator.Output" :key="output.Identifier" class="output-field">
                <label>{{ output.Title }}</label>
                
                <!-- 选择输出格式 -->
                <el-select v-if="output.Identifier === 'output_txt'" v-model="selectedFormat"
                           placeholder="Select Output Format"
                           class="uniform-width">
                    <el-option v-for="format in output.ComplexData.Format" :key="format.mimeType"
                               :label="format.mimeType" :value="format.mimeType">
                    </el-option>
                </el-select>
                
                <el-button v-else-if="output.DataType === 'ComplexData' && !output.hasDownloadButton" target="_blank"
                           @click="executeOperator"
                           type="primary" class="download-button uniform-width">
                    Download Results
                </el-button>
                
                <el-select
                    v-else-if="output.DataType === 'LiteralData' && output.LiteralData.LiteralDataDomain[0].AllowedValues?.length"
                    v-model="outputValues[output.Identifier]" placeholder="Please Select" class="uniform-width">
                    <el-option v-for="(value, index) in output.LiteralData.LiteralDataDomain[0].AllowedValues"
                               :key="index" :label="value[Object.keys(value)[0]]" :value="Object.keys(value)[0]">
                    </el-option>
                </el-select>
                
                <el-input-number
                    v-else-if="output.DataType === 'LiteralData' && ['int', 'float'].includes(output.LiteralData.LiteralDataDomain[0].DataType.content)"
                    v-model="outputValues[output.Identifier]" :placeholder="output.Abstract" :min="0"
                    class="uniform-width">
                </el-input-number>
                
                <el-input
                    v-else-if="output.DataType === 'LiteralData' && output.LiteralData.LiteralDataDomain[0].DataType.content === 'string'"
                    v-model="outputValues[output.Identifier]" :placeholder="output.Abstract" class="uniform-width">
                </el-input>
                
                <div
                    v-else-if="output.DataType === 'LiteralData' && output.LiteralData.LiteralDataDomain[0].DataType.content === 'boolean'"
                    class="boolean-output">
                    <el-switch v-model="outputValues[output.Identifier]"
                               :active-text="output.LiteralData.LiteralDataDomain[0].TrueLabel"
                               :inactive-text="output.LiteralData.LiteralDataDomain[0].FalseLabel" :active-value="true"
                               :inactive-value="false">
                    </el-switch>
                    <span class="bool-description">{{ output.Abstract }}</span>
                </div>
            </div>
        </div>
        
        <!-- 执行按钮 -->
        <el-button v-if="operator.Output.every(o => o.DataType !== 'ComplexData' || o.hasDownloadButton)"
                   class="execute-button uniform-width" type="primary" @click="executeOperator"
                   :disabled="!isValidInputs">
            Execute Operator
        </el-button>
    
    </div>
</template>

<script setup>
import {ref, watch} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import {ArrowLeft} from '@element-plus/icons-vue';
import axios from 'axios';
import {ElMessage} from 'element-plus';

const operator = ref(null);
const router = useRouter();
const route = useRoute();
const inputValues = ref({});
const outputValues = ref({});
const selectedFormat = ref(null);
const mode = ref('sync');
const uploadRefs = ref({}); // 用于存储所有 el-upload 的引用
const isValidInputs = ref(false); // 用于动态检查输入完整性

watch(
    () => route.params.Identifier,
    async (newIdentifier) => {
        if (newIdentifier) {
            try {
                const response = await axios.get(`/api/processes/${newIdentifier}`);
                operator.value = response.data;
                console.log("当前算子信息：", response.data);
                initializeParameterinValues();
                initializeParameteroutValues();
            } catch (error) {
                console.error("获取算子信息失败:", error);
            }
        }
    },
    {immediate: true}
);

function doClear() {
    // 清空所有上传文件的列表
    Object.values(uploadRefs.value).forEach((uploadInstance) => {
        if (uploadInstance && uploadInstance.clearFiles) {
            uploadInstance.clearFiles();
        }
    });
    
    // 返回算子工具箱
    router.push({name: 'OperatorToolbox'});
}

// 在模板中动态注册 refs
function registerUploadRef(refName, refInstance) {
    if (refInstance) {
        uploadRefs.value[refName] = refInstance;
    }
}


// 初始化输入参数的值
function initializeParameterinValues() {
    if (operator.value) {
        operator.value.Input.forEach((input) => {
            inputValues.value[input.Identifier] = input.LiteralData?.LiteralDataDomain[0]?.DefaultValue || '';
        });
    }
}

// 初始化输出参数的值
function initializeParameteroutValues() {
    if (operator.value) {
        operator.value.Output.forEach((output) => {
            outputValues.value[output.Identifier] = output.LiteralData?.LiteralDataDomain[0]?.DefaultValue || '';
            if (output.DataType === 'ComplexData') {
                output.hasDownloadButton = !!output.hasDownloadButton;
            }
        });
    }
}

// 获取支持的格式
function getSupportedFormats(complexData) {
    return complexData?.Format?.map(f => f.mimeType).join(',') || '';
}

// 上传成功的回调
function handleUploadSuccess(response, file, identifier) {
    console.log("文件上传成功回调触发", response);
    console.log("上传的 Identifier:", identifier);  // 确保 identifier 是上传文件时传递的值
    
    ElMessage({
        message: 'Files uploaded successfully！',
        type: 'success',
    });
    
    const filenames = response.data?.filenames || response.filenames;
    if (!filenames || filenames.length === 0) {
        console.error("文件上传成功，但未找到 filenames", response);
        return;
    }
    
    const fileUrl = `http://8.137.39.2:5000/inputs/${filenames[0]}`;
    console.log("生成的文件URL:", fileUrl);
    
    // 确保 identifier 的值是一个数组，用于存储多个文件
    inputValues.value[identifier] = inputValues.value[identifier] || [];
    
    // 检查是否已经存在相同的文件，避免重复添加
    const isDuplicate = inputValues.value[identifier].some(item => item.url === fileUrl);
    if (isDuplicate) {
        console.warn("重复的文件已上传:", fileUrl);
        return;
    }
    
    // 将当前文件信息追加到数组中
    inputValues.value[identifier].push({
        name: file.name,
        size: file.size,
        url: fileUrl,
        Identifier: identifier, // 确保保存上传时的参数标识符
    });
    
    // 输出绑定的文件集合
    console.log("当前 identifier 累积的文件信息:", inputValues.value[identifier]);
}

function validateInputs() {
    
    if (operator.value) {
        isValidInputs.value = operator.value.Input.every((input) => {
            const value = inputValues.value[input.Identifier];
            return input.minOccurs === 0 || (value && value !== '');
        });
    }
}

// <!--src/components/OperatorIdentifier-->
// 执行操作的函数
async function executeOperator() {
    validateInputs();
    if (!isValidInputs.value) {
        ElMessage.error("Please fill in all required parameters!");
        return;
    }
    console.log("执行操作开始");
    
    console.log("执行算子", inputValues.value);
    const inputs = {};
    operator.value.Input.forEach(input => {
        const identifier = input.Identifier;
        const value = inputValues.value[identifier];
        
        if (identifier !== 'OUTPUT' && value) {
            if (input.DataType === "ComplexData") {
                const href = value[0]?.url;
                if (href) {
                    inputs[identifier] = {
                        type: 'reference',
                        href: href
                    };
                } else {
                    console.warn("文件没有 URL:", value);
                }
            } else {
                inputs[identifier] = value;
            }
        }
    });
    
    const requestData = {
        identifier: operator.value.Identifier,
        mode: mode.value,
        inputs: inputs
    };
    
    console.log("准备发送的请求数据:", requestData);
    
    try {
        const response = await axios.post('/api/jobs', requestData);
        console.log("执行成功，响应数据:", response.data);
        
        
    } catch (error) {
        console.error("执行失败:", error);
    }
}

// 监控输入值以动态更新按钮状态
watch(inputValues, () => {
    let isValidInputs;
    isValidInputs.value = Object.values(inputValues.value).every(value => value !== '');
});
</script>

<style scoped>
.operator-identifier {
    padding: 20px;
    height: calc(100vh - 100px);
    overflow-y: auto;
    width: 320px;
    position: relative;
    border-left: 1px solid #dcdfe6;
}

.back-button {
    font-size: 16px;
    color: #409EFF;
    display: flex;
    align-items: center;
    margin-bottom: 20px;
}

.operator-abstract {
    margin-top: 20px;
    font-size: 14px;
    line-height: 1.5;
}

.input-section,
.output-section {
    margin-top: 20px;
}

.input-field,
.output-field {
    margin-bottom: 15px;
}

.abstract-text {
    font-size: 8px;
    color: #888;
    margin-left: 4px;
}

.boolean-input {
    display: flex;
    align-items: center;
}

.bool-description {
    font-size: 12px;
    color: #666;
    margin-left: 8px;
    /* 与开关保持合适的间距 */
    line-height: 1.4;
    max-width: 80%;
}

.uploaded-file {
    margin-left: 10px;
    color: #409EFF;
    cursor: pointer;
}

/* 设置统一的宽度 */
.uniform-width {
    width: 320px;
}

/* 设置下载文件按钮的宽度 */
.upload-button,
.execute-button,
.download-button {
    margin-top: 10px;
    width: 320px;
    /* 改为100%以统一宽度 */
}

.input-field label,
.output-field label {
    display: block;
    margin-bottom: 8px;
    /* 设置标题与控件之间的距离 */
    font-weight: bold;
    /* 让标题更显眼 */
}

.upload-button {
    margin-top: 10px;
    width: 320px;
    background-color: #409EFF;
    /* 上传按钮颜色 */
    color: white;
    /* 字体颜色 */
}

.download-button {
    margin-top: 10px;
    width: 320px;
    background-color: #67C23A;
    /* 下载按钮颜色 */
    color: white;
    /* 字体颜色 */
}

.input-field .el-input,
.input-field .el-input-number,
.input-field .el-select,
.output-field .el-input,
.output-field .el-select,
.boolean-input,
.upload-button,
.download-button {
    margin-top: 5px;
    /* 控件与上方标题的距离 */
}
</style>