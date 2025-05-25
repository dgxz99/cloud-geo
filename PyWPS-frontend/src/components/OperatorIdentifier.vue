<!--src/components/OperatorIdentifier-->
<template>
    <div class="operator-identifier" v-if="operator">
        <!-- 返回按钮 -->
        <el-button type="text" class="back-button" @click="doClear()">
            <el-icon>
                <ArrowLeft />
            </el-icon>
            <span style="font-size: 20px;">{{ operator.data.Identifier }}</span>
        </el-button>

        <!-- 算子描述 -->
        <div class="operator-abstract">{{ operator.data.Abstract }}</div>

        <!-- 输入参数部分 -->
        <div class="input-section">
            <h3>Input Parameters</h3>
            <div v-for="input in operator.data.Input.filter(i => i.Identifier !== 'OUTPUT' && i.Identifier !== 'output')"
                :key="input.Identifier" class="input-field">
                <label>
                    {{ input.Identifier }}
                    <span v-if="input.minOccurs >= 1" style="color: red;">*</span>
                </label>
                <!-- 上传文件控件 -->
                <el-upload v-if="input.DataType === 'ComplexData'"
                    :ref="(ref) => registerUploadRef('upload-' + input.Identifier, ref)"
                    :data="{ identifier: input.Identifier }" :accept="getSupportedFormats(input.ComplexData)"
                    class="uniform-width" action="/api/file/upload"
                    :on-success="(response, file, fileList) => handleUploadSuccess(response, file, input.Identifier)"
                    :on-error="handleUploadError">
                    <el-button class="upload-button uniform-width" type="primary">Upload File</el-button>
                </el-upload>

                <!-- 输入参数选择 -->
                <el-select :teleported="false"
                    v-if="(input.Identifier === 'OUTPUT' || input.Identifier === 'output') && input.DataType === 'ComplexData'"
                    v-model="inputValues[input.Identifier]" placeholder="Select Output Format" class="uniform-width">
                    <el-option v-for="(format, index) in input.ComplexData.Format" :key="index" :label="format.mimeType"
                        :value="format.mimeType">
                    </el-option>
                </el-select>

                <!-- LiteralData 类型的输入 -->
                <el-select :teleported="false"
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
            <h3>Execution Mode</h3>
            <el-radio-group v-model="mode" class="uniform-width">
                <el-radio label="sync">Synchronous</el-radio>
                <el-radio label="async">Asynchronous</el-radio>
            </el-radio-group>
        </div>

        <!-- 输出参数部分 -->
        <div class="output-section">
            <h3>Output Parameters</h3>
            <div v-for="output in operator.data.Output" :key="output.Identifier" class="output-field">
                <label>{{ output.Title }}</label>

                <!-- 选择输出格式 -->
                <el-select v-if="output.Identifier === 'output_txt'" v-model="selectedFormat" :teleported="false"
                    placeholder="Select Output Format" class="uniform-width">
                    <el-option v-for="format in output.ComplexData.Format" :key="format.mimeType"
                        :label="format.mimeType" :value="format.mimeType">
                    </el-option>
                </el-select>

                <el-button v-else-if="output.DataType === 'ComplexData' && !output.hasDownloadButton" target="_blank"
                    @click="executeOperator" type="primary" class="download-button uniform-width">
                    Execute Operator
                </el-button>

                <el-select :teleported="false"
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
        <el-button v-if="operator.data.Output.every(o => o.DataType !== 'ComplexData' || o.hasDownloadButton)"
            class="execute-button uniform-width" type="primary" @click="executeOperator" :disabled="!isValidInputs">
            Execute Operator
        </el-button>
    </div>
</template>

<script setup>
import { inject, ref, watch, defineProps, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ArrowLeft } from '@element-plus/icons-vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { useStore } from 'vuex';

const operator = ref(null);
const router = useRouter();
const route = useRoute();
const store = useStore();
const inputValues = ref({});
const outputValues = ref({});
const selectedFormat = ref(null);
const mode = ref('sync');
const uploadRefs = ref({});
const isValidInputs = ref(false);
const toolboxControl = inject('toolboxControl');
const props = defineProps({
    toggleToolbox: Function
});

watch(
    () => route.params.Identifier,
    async (newIdentifier) => {
        if (newIdentifier) {
            try {
                const response = await axios.get(`/processes/${newIdentifier}`);
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

function doClear() {
    Object.values(uploadRefs.value).forEach((uploadInstance) => {
        if (uploadInstance && uploadInstance.clearFiles) {
            uploadInstance.clearFiles();
        }
    });
    router.push({ name: 'OperatorToolbox' });
}

function registerUploadRef(refName, refInstance) {
    if (refInstance) {
        uploadRefs.value[refName] = refInstance;
    }
}

function initializeParameterinValues() {
    if (operator.value) {
        operator.value.data.Input.forEach((input) => {
            inputValues.value[input.Identifier] = input.LiteralData?.LiteralDataDomain[0]?.DefaultValue || '';
        });
    }
}

function initializeParameteroutValues() {
    if (operator.value) {
        operator.value.data.Output.forEach((output) => {
            outputValues.value[output.Identifier] = output.LiteralData?.LiteralDataDomain[0]?.DefaultValue || '';
            if (output.DataType === 'ComplexData') {
                output.hasDownloadButton = !!output.hasDownloadButton;
            }
        });
    }
}

function getSupportedFormats(complexData) {
    return complexData?.Format?.map(f => f.mimeType).join(',') || '';
}

function handleUploadSuccess(response, file, identifier) {

    ElMessage({
        message: 'Files uploaded successfully！',
        type: 'success',
    });

    console.log("handleUploadSuccess:", response);

    let href = response.data?.href || '';

    if (!href) {
        let filenames = response.data?.filenames;
        href = filenames[0].href;
    }

    console.log("href:", href);

    const fileUrl = href;
    inputValues.value[identifier] = inputValues.value[identifier] || [];
    const isDuplicate = inputValues.value[identifier].some(item => item.url === fileUrl);
    if (!isDuplicate) {
        inputValues.value[identifier].push({
            name: file.name,
            size: file.size,
            url: fileUrl,
            Identifier: identifier,
        });
    }
}

function validateInputs() {
    if (operator.value) {
        isValidInputs.value = operator.value.data.Input.every((input) => {
            const value = inputValues.value[input.Identifier];
            return input.minOccurs === 0 || (value && value !== '');
        });
    }
}

async function executeOperator() {
    validateInputs();
    if (!isValidInputs.value) {
        ElMessage.error("Please fill in all required parameters!");
        return;
    }

    props.toggleToolbox(null);
    if (toolboxControl) {
        nextTick(() => {
            toolboxControl.showToolboxAndSwitchToProcessedData();
        });
    }

    const inputs = {};
    operator.value.data.Input.forEach(input => {
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
                }
            } else {
                inputs[identifier] = value;
            }
        }
    });

    const requestData = {
        identifier: operator.value.data.Identifier,
        mode: mode.value,
        inputs: inputs
    };

    const taskId = Date.now();
    const initialTask = {
        jobId: taskId,
        operatorName: operator.value.data.Identifier,
        status: 'running',
    };

    store.commit('operator/ADD_TASK', initialTask);

    try {
        const response = await axios.post('/jobs', requestData);
        store.commit('operator/UPDATE_TASK_STATUS', {
            taskId,
            status: response.data.status || 'succeeded',
            completionTime: response.data.completionTime || new Date().toISOString(),
            errorMessage: null,
            output: response.data.data.output
        });
    } catch (error) {
        store.commit('operator/UPDATE_TASK_STATUS', {
            taskId,
            status: 'failed',
            errorMessage: error.response?.data || error.message,
            completionTime: new Date().toISOString(),
        });
    }
}

watch(inputValues, () => {
    isValidInputs.value = Object.values(inputValues.value).every(value => value !== '');
});
</script>



<style>
.el-input-number .el-input__wrapper {
    background-color: #2d2d2d;
    box-shadow: 0 0 0 1px #444 inset;
}

.el-input-number .el-input-number__decrease,
.el-input-number .el-input-number__increase {
    background-color: #2d2d2d;
    border-color: #444;
    color: #e0e0e0;
}

.el-input-number .el-input-number__decrease:hover,
.el-input-number .el-input-number__increase:hover {
    background-color: #444;
    color: #e0e0e0;
}

.el-input-number .el-input-number__decrease:active,
.el-input-number .el-input-number__increase:active {
    background-color: #666;
}

.el-input-number .el-input__inner {
    background-color: #2d2d2d;
    color: #e0e0e0;
}

/* 下拉选择框样式 */
.el-select-dropdown {
    background-color: #2d2d2d;
    border: 1px solid #444;
}

.el-select-dropdown__item {
    color: #e0e0e0;
    background-color: #2d2d2d;
}

.el-select-dropdown__item.hover,
.el-select-dropdown__item:hover {
    background-color: #444;
}
</style>

<style scoped>
.operator-identifier {
    padding: 20px;
    height: calc(100vh - 100px);
    overflow-y: auto;
    width: 320px;
    position: relative;
    background-color: #1e1e1e;
    color: #e0e0e0;
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
    color: #e0e0e0;
}

.input-section,
.output-section {
    margin-top: 20px;
    color: #e0e0e0;
}

.input-field,
.output-field {
    margin-bottom: 15px;
}


/* 开关样式 */
.el-switch {
    --el-switch-on-color: #409EFF;
    --el-switch-off-color: #666;
}


/* 输入框样式 */
.el-input {
    --el-input-bg-color: #2d2d2d;
    --el-input-text-color: #e0e0e0;
    --el-input-border-color: #444;
    --el-input-hover-border-color: #666;
    --el-input-focus-border-color: #409EFF;
}

/* 其他样式保持不变 */
.uniform-width {
    width: 320px;
}

.upload-button,
.execute-button,
.download-button {
    margin-top: 10px;
    width: 320px;
}

.input-field label,
.output-field label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
}

.upload-button {
    background-color: #409EFF;
}

.download-button {
    background-color: #67C23A;
    border: #67C23A;
}

:deep(.el-select__wrapper) {
    background: #2d2d2d;
    box-shadow: 0 0 0 1px #444;
}
</style>