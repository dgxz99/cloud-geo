<template>
    <div class="operator-identifier" v-if="operator">
        <!-- 返回按钮 -->
        <el-button type="text" class="back-button" @click="$router.push({ name: 'OperatorToolbox' })">
            <el-icon>
                <ArrowLeft />
            </el-icon>
            <span style="font-size: 20px;">{{ operator.Identifier }}</span>
        </el-button>

        <!-- 算子描述 -->
        <div class="operator-abstract">{{ operator.Abstract }}</div>

        <!-- 输入参数部分 -->
        <div class="input-section">
            <h3>输入参数</h3>
            <div v-for="input in operator.Input" :key="input.Identifier" class="input-field">
                <label>{{ input.Title }}</label>
                <!-- 上传文件控件 -->
                <el-upload
                    v-if="input.DataType === 'ComplexData' && input.Identifier !== 'OUTPUT' && input.Identifier !== 'output'"
                    :http-request="customUploadRequest" :accept="getSupportedFormats(input.ComplexData)"
                    show-file-list="false" class="uniform-width">
                    <el-button class="upload-button uniform-width" type="primary">上传文件</el-button>
                </el-upload>


                <!-- 输出参数选择 -->
                <el-select
                    v-if="(input.Identifier === 'OUTPUT' || input.Identifier === 'output') && input.DataType === 'ComplexData'"
                    v-model="inputValues[input.Identifier]" placeholder="选择输出格式" class="uniform-width">
                    <el-option v-for="(format, index) in input.ComplexData.Format" :key="index" :label="format.mimeType"
                        :value="format.mimeType">
                    </el-option>
                </el-select>

                <!-- LiteralData 类型的输入 -->
                <el-select
                    v-else-if="input.DataType === 'LiteralData' && input.LiteralData.LiteralDataDomain[0].AllowedValues?.length"
                    v-model="inputValues[input.Identifier]" placeholder="请选择" class="uniform-width">
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

                <div v-else-if="input.DataType === 'LiteralData' && input.LiteralData.LiteralDataDomain[0].DataType.content === 'boolean'"
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
             <h3>mode</h3>
            <el-radio-group v-model="mode" class="uniform-width">
                <el-radio label="sync">sync</el-radio>
                <el-radio label="async">async</el-radio>
            </el-radio-group>
        </div>

        <!-- 输出参数部分 -->
        <div class="output-section">
            <h3>输出参数</h3>
            <div v-for="output in operator.Output" :key="output.Identifier" class="output-field">
                <label>{{ output.Title }}</label>

                <!-- 选择输出格式 -->
                <el-select v-if="output.Identifier === 'output_txt'" v-model="selectedFormat" placeholder="选择输出格式"
                    class="uniform-width">
                    <el-option v-for="format in output.ComplexData.Format" :key="format.mimeType"
                        :label="format.mimeType" :value="format.mimeType">
                    </el-option>
                </el-select>

                <el-button v-else-if="output.DataType === 'ComplexData' && !output.hasDownloadButton" target="_blank" @click="executeOperator"
                    type="primary" class="download-button uniform-width">
                    下载结果
                </el-button>

                <el-select
                    v-else-if="output.DataType === 'LiteralData' && output.LiteralData.LiteralDataDomain[0].AllowedValues?.length"
                    v-model="outputValues[output.Identifier]" placeholder="请选择" class="uniform-width">
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

                <div v-else-if="output.DataType === 'LiteralData' && output.LiteralData.LiteralDataDomain[0].DataType.content === 'boolean'"
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
            class="execute-button uniform-width" type="primary" @click="executeOperator" :disabled="!isValidInputs">
            执行
        </el-button>
    </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { ArrowLeft } from '@element-plus/icons-vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';

const route = useRoute();
const operator = ref(null);
const inputValues = ref({});
const outputValues = ref({});
const selectedFormat = ref(null);
// 定义执行模式的响应变量，默认值设置为 'sync' 或 'async'，取决于你的默认需求
const mode = ref('sync');


// 用于验证输入参数是否有效
const isValidInputs = ref(true);

// 监视路由参数中的 Identifier 变化，以便动态加载算子信息
watch(
    () => route.params.Identifier,
    async (newIdentifier) => {
        if (newIdentifier) {
            try {
                const response = await axios.get(`/api/processes/${newIdentifier}`);
                operator.value = response.data;
                initializeParameterinValues();
                initializeParameteroutValues();
            } catch (error) {
                console.error("获取算子信息失败:", error);
            }
        }
    },
    { immediate: true }
);

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
function handleUploadSuccess(response, file) {
    ElMessage({
        message: '上传文件成功！',
        type: 'success',
    })

    console.log("上传响应数据:", response);
    console.log("上传的文件信息:", file);

    // 根据上传返回的数据更新 inputValues 或其他状态
    if (response && response.filename) {
        const filename = response.filename;
        let baseUrl;

        //  使用完整服务器 URL
        baseUrl = 'http://8.137.39.2:5000/inputs/';
        this.fileUrl = `${baseUrl}${filename}`;

    } else {
        console.error('文件上传成功，但未找到 filename');
    }
}

// 自定义上传请求
function customUploadRequest({ file, data }) {
    // 创建 FormData 对象来包含文件和额外的数据
    const formData = new FormData();
    formData.append('file', file);
    formData.append('identifier', data.identifier);

    axios.post('/api/upload', formData)
        .then(response => handleUploadSuccess(response, file))
        .catch(error => handleUploadError(error, file));
}

// 上传失败的回调
function handleUploadError(error, file) {
    ElMessage({
        message: '上传文件失败！',
        type: 'error',
    })
    console.error("文件上传失败回调触发:");
    console.error("错误信息:", error);
    console.error("上传的文件信息:", file);
}

// 执行操作的函数
async function executeOperator() {
    console.log("执行算子", inputValues.value);
    if (!operator.value) {
        console.error('未选择操作符，无法执行算子');
        return;
    }

    const requestData = {
        identifier: operator.value.Identifier,
        mode: mode.value, // 使用用户选择的执行模式
        inputs: {
            INPUT: {
                type: 'reference',
                href: inputValues.value // 假设用户文件URL已设置在 inputValues 中
            }
        }
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