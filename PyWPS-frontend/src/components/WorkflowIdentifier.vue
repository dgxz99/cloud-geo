<!--src/components/WorkflowIdentifier-->
<template>
    <div class="workflow-identifier" v-if="operator">
        <!-- 返回按钮 -->
        <el-button type="text" class="back-button" @click="doClear()">
            <el-icon>
                <ArrowLeft />
            </el-icon>
            <span style="font-size: 20px;">{{ operator.data.Identifier }}</span>
        </el-button>

        <!-- 输入参数部分 -->
        <div class="input-section">
            <h3>Input Parameters</h3>
            <div v-for="input in (operator.data.Input || []).filter(i => i.Identifier !== 'OUTPUT' && i.Identifier !== 'output')"
                :key="input.Identifier" class="input-field">
                <label>
                    {{ input.Identifier }}
                    <span v-if="input.minOccurs >= 1" style="color: red;">*</span>
                </label>
                <!-- 上传文件控件 -->
                <el-upload v-if="input.DataType === 'ComplexData'"
                    :ref="(ref) => registerUploadRef('upload-' + input.Identifier, ref)"
                    :data="{ identifier: input.Identifier }" :accept="getSupportedFormats(input.ComplexData)"
                    class="uniform-width" action="/api/upload"
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
        <el-button class="save-button uniform-width" type="success" @click="saveConfiguration">
            Save Configuration
        </el-button>
    </div>
</template>

<script setup>
// 导入 Vue 和 Element Plus 相关模块
import { inject, ref, watch, defineProps, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ArrowLeft } from '@element-plus/icons-vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { useStore } from 'vuex';

import { v4 as uuidv4 } from 'uuid';

const generateUniqueId = () => {
    return uuidv4();
};

// 注入 resetView
const resetView = inject('resetView');
function doClear() {
    // 调用 resetView 以重置状态
    if (resetView) {
        resetView();
    }
    router.push({ name: 'OperatorWorkflow' });
}

// 初始化可变数据对象，用于后续的数据绑定和状态管理
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

// 定义组件接收的属性，此处的属性用于控制工具箱的显示
const props = defineProps({
    toggleToolbox: Function
});

// 监听路由参数变化，根据 operatorId 获取算子详情
watch(
    [() => route.params.workflowId, () => route.params.operatorId],
    async ([workflowId, operatorId]) => {
        console.log('开始加载节点配置', { workflowId, operatorId })
        try {
            const apiUrl = `/api/processes/${operatorId}`
            console.log('请求地址:', apiUrl)
            const response = await axios.get(apiUrl)
            console.log('响应数据结构:', response.data)
            operator.value = response.data
        } catch (error) {
            console.error("请求失败详情:", error.config)
        }
    }
)

function registerUploadRef(refName, refInstance) {
    if (refInstance) {
        uploadRefs.value[refName] = refInstance;
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

    const filenames = response.data?.filenames || response.filenames;
    if (!filenames || filenames.length === 0) {
        console.error("文件上传成功，但未找到 filenames", response);
        return;
    }

    const fileUrl = `http://dev.swsk33-mcs.top:9002/inputs/${filenames[0]}`;
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
        const response = await axios.post('/api/jobs', requestData);
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

const saveConfiguration = () => {
    if (!operator.value) {
        ElMessage.warning('No operator configuration to save!');
        return;
    }

    const operatorDetail = operator.value; // 包含算子信息（例如 data.Input、data.Output、data.Identifier 等）
    const operatorIdentifier = operatorDetail.data.Identifier;

    // ① 计算用户配置的输入（inputValues）
    const computedInputValues = Object.entries(inputValues.value).reduce((acc, [key, value]) => {
        if (Array.isArray(value)) {
            // 如果是上传的文件列表
            acc[key] = {
                files: value.map(item => ({
                    name: item.name,
                    size: item.size,
                    url: item.url,
                    identifier: item.Identifier
                }))
            };
        } else if (value !== null && value !== undefined && value !== '') {
            // 如果是 LiteralData 类型的配置
            acc[key] = { value: value };
        }
        return acc;
    }, {});

    // ② 合并原始的 Input 元数据和用户配置，同时加入默认值（若未被用户覆盖）
    const mergedInputParams = {};
    if (operatorDetail.data.Input && operatorDetail.data.Input.length > 0) {
        operatorDetail.data.Input.forEach(input => {
            const key = input.Identifier;
            // 构建基础的元数据对象
            mergedInputParams[key] = {
                type: input.DataType, // "ComplexData" 或 "LiteralData"
                minOccurs: input.minOccurs || 0,
                maxOccurs: input.maxOccurs || 1,
                connected: 0,
                supportedFormats: (input.DataType === 'ComplexData' &&
                    input.ComplexData &&
                    input.ComplexData.Format)
                    ? input.ComplexData.Format.map(f => f.mimeType)
                    : undefined,
                // 如果用户已经提供配置则合并进去
                ...computedInputValues[key]
            };
            // 如果用户未提供配置且是 LiteralData 类型，并且存在默认值，则添加默认值
            if (!computedInputValues[key] && input.DataType === 'LiteralData' && input.defaultValue !== undefined) {
                mergedInputParams[key].value = input.defaultValue;
            }
        });
    } else {
        // 如果原始数据中没有 Input，则直接使用用户配置
        Object.assign(mergedInputParams, computedInputValues);
    }

    // ③ 合并原始的 Output 元数据和用户配置（如果有）
    const mergedOutputParams = {};
    if (operatorDetail.data.Output && operatorDetail.data.Output.length > 0) {
        operatorDetail.data.Output.forEach(output => {
            const key = output.Identifier;
            mergedOutputParams[key] = {
                type: output.DataType,
                minOccurs: output.minOccurs || 0,
                maxOccurs: output.maxOccurs || 1,
                connected: 0,
                supportedFormats: (output.DataType === 'ComplexData' &&
                    output.ComplexData &&
                    output.ComplexData.Format)
                    ? output.ComplexData.Format.map(f => f.mimeType)
                    : undefined,
                ...(outputValues.value[key] ? { value: outputValues.value[key] } : {})
            };
            // 同样对于 LiteralData，如果未由用户提供值且有默认值
            if (!outputValues.value[key] && output.DataType === 'LiteralData' && output.defaultValue !== undefined) {
                mergedOutputParams[key].value = output.defaultValue;
            }
        });
    } else {
        Object.assign(mergedOutputParams, outputValues.value);
    }

    // ④ 构建完整的算子配置对象（包含算子信息和配置）
    const newOperatorConfig = {
        id: operatorDetail.id, // 原始算子的 id
        identifier: operatorIdentifier,
        inputParams: mergedInputParams,
        outputParams: mergedOutputParams,
        executionMode: mode.value,
        selectedFormat: selectedFormat.value
    };

    // ⑤ 从 Vuex 中获取所有已保存的算子配置，根据 identifier 判断是否已经存在
    const allConfigs = store.getters['workflow/getWorkflowNodes'];
    let existingConfigIndex = allConfigs.findIndex(config => config.identifier === operatorIdentifier);

    // ⑥ 保存（如果已存在则更新，不存在则新增）
    store.dispatch('workflow/saveOperatorConfig', { existingConfigIndex, newOperatorConfig });

    console.groupCollapsed('🚀 Saved Operator Configuration');
    console.log('Operator Configuration:', newOperatorConfig);
    console.log('All Configurations:', store.getters['workflow/getWorkflowNodes']);
    console.groupEnd();

    ElMessage.success('Configuration saved successfully!');
};




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
.workflow-identifier {
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