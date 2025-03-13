<!-- src/components/OperatorWorkflow.vue -->
<template>
    <div class="operator-workflow">
        <div class="layout-container">
            <!-- 左侧区域 -->
            <div class="left-container">
                <!-- 工具栏部分 -->
                <div class="toolbar-container">
                    <ToolBar @tool-change="setTool" />
                </div>
                <!-- 主内容部分 -->
                <div class="content-container" ref="paperRef" @dragover.prevent @drop="onDrop">
                </div>
                <!-- 动态参数弹窗 -->
                <ParamPopup v-if="showParams" :visible="true" :position="popupPosition" :paramList="currentParams"
                    @param-selected="handleParamSelected" />
            </div>
        </div>
        <!-- 右侧区域：工具箱 -->
        <div class="toolbox-container" v-show="shouldShowToolbox">
            <el-tabs v-model="activeTab">
                <el-tab-pane label="Processing Toolbox" name="toolbox">
                    <el-input v-model="searchQuery" placeholder="Search operators..." clearable :prefix-icon="Search"
                        class="search-box"></el-input>
                    <ul v-if="!loading">
                        <li v-for="operator in filteredOperators" :key="operator.Identifier">
                            <!-- 添加 draggable 和 dragstart 事件 -->
                            <el-button type="text" draggable="true" @dragstart="onDragStart(operator, $event)">
                                {{ operator.Identifier }}
                            </el-button>
                        </li>
                    </ul>
                    <p v-else-if="filteredOperators.length === 0">No operators found.</p>
                </el-tab-pane>
            </el-tabs>
        </div>
    </div>
</template>

<script setup>
import ToolBar from './WorkflowToolBar.vue';
import { ref, computed, onMounted, nextTick, onActivated } from "vue";
import { useStore } from "vuex";
import * as joint from "jointjs";
import axios from 'axios'; // 引入 axios
import { ElMessage } from 'element-plus';
import { getGlobalGraph, setGlobalGraph, getGlobalPaper, setGlobalPaper } from '../joints'
import { nanoid } from 'nanoid'

import ParamPopup from './ParamPopup.vue';
import { inject } from 'vue';

const showWorkflowIdentifier = inject('showWorkflowIdentifier');

const showParams = ref(false);
const popupPosition = ref({ x: 0, y: 0 });
const currentParams = ref([]);

// 活跃选项卡的绑定值
const activeTab = ref("toolbox");

// 搜索框绑定的输入值
const searchQuery = ref("");

// 初始化 Vuex 存储
const store = useStore();

// 计算属性，从 Vuex 存储中获取算子列表
const operators = computed(() => store.state.operator.operators);

// 计算属性，从 Vuex 存储中获取加载状态
const loading = computed(() => store.state.operator.loading);

// 筛选后的算子列表（实时更新）
const filteredOperators = computed(() => {
    if (!searchQuery.value) {
        return operators.value;
    }
    return operators.value.filter((operator) =>
        operator.Identifier.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
});

// JointJS 画布和图形的引用
const paperRef = ref(null);

const tool = ref('select'); // 当前工具

// 新增状态：跟踪等待参数选择的连接
const pendingConnection = ref(null);

// 新增代码部分
import { useRoute } from 'vue-router';

const route = useRoute();

// 计算是否显示工具箱
const shouldShowToolbox = computed(() => {
    // 当处于工作流模式且不在算子详情页时显示
    return route.name !== 'WorkflowIdentifier';
});

// 当组件挂载时，初始化流程图
let paper = null;

const initializePaper = () => {
    const paperElement = paperRef.value; // 保持指向DOM元素
    if (!paperElement) {
        console.error("画布元素未挂载");
        return;
    }
    // 清除现有Paper实例的正确方式
    const existingPaper = getGlobalPaper();
    if (existingPaper && existingPaper.el) {
        existingPaper.remove();
    }
    const width = paperElement.offsetWidth;
    const height = paperElement.offsetHeight;
    const graph = new joint.dia.Graph();

    paper = new joint.dia.Paper({
        // el: document.getElementById('paper-container'),
        el: paperElement,
        model: graph,
        width: width,
        height: height,
        gridSize: 10,
        drawGrid: true,
        interactive: {
            linkMove: false
        },
        linkingMode: 'directed'
    });


    // 重新设置事件监听
    nextTick(() => {
        setTool(tool.value);
    });

    // 监听链接删除事件
    paper.model.on('remove', (cell) => {
        if (cell.isLink()) {
            const targetParam = cell.get('params')?.targetParam;
            const targetNode = cell.getTargetElement();

            if (targetParam && targetNode) {
                const params = targetNode.get('inputParams');
                if (params[targetParam]?.connected > 0) {
                    params[targetParam].connected -= 1;
                    targetNode.set('inputParams', { ...params });
                }
            }
        }
    });

    // 2. 通过全局状态管理Paper实例（joints.js模块存储）
    setGlobalPaper(paper);
};


// 在创建工作流或进入工作流页面时生成ID
onMounted(() => {
    const newWorkflowId = nanoid();
    store.commit('workflow/SET_ACTIVE_WORKFLOW', newWorkflowId);
    console.log('生成工作流ID:', newWorkflowId);
});

onMounted(() => {
    initializePaper();
});

onActivated(() => {
    // 如果 paper 无效则重新初始化
    if (!paper || !paper.el || !paper.model) {
        initializePaper();
    }
});


// 添加状态变量来跟踪连接过程
const connectionSource = ref(null);

const handleOperatorClick = (operatorModel) => {
    const workflowId = store.state.workflow.activeWorkflowId;
    const operatorId = operatorModel.get('operatorIdentifier');

    if (showWorkflowIdentifier) {
        showWorkflowIdentifier(workflowId, operatorId);
    } else {
        console.error('showWorkflowIdentifier 未能注入');
    }
};

/**
 * 判断从目标节点到源节点的父算子是否存在路径（环路检查）
 * @param {joint.dia.Graph} graph 画布的Graph对象
 * @param {joint.shapes.standard.Link} sourceParentNode 源节点的父算子节点（必须是算子节点）
 * @param {joint.shapes.standard.Node} targetNode 连接目标的算子节点
 * @returns {boolean} 是否存在环路
 */
const isCreatingCycle = (graph, sourceParentNode, targetNode) => {
    // 若源parent节点不存在（如意外情况），直接返回
    if (!sourceParentNode) return false;

    const visited = new Set();
    const queue = [targetNode]; // 起始点是要连接到的新目标节点

    // BFS遍历所有下游节点
    while (queue.length > 0) {
        const currentNode = queue.shift();
        if (visited.has(currentNode.id)) continue;
        visited.add(currentNode.id);

        // 只要找到到源父算子的路径，立即判定为环路
        if (currentNode.id === sourceParentNode.id) {
            return true;
        }

        // 获取当前节点所有流出连接（输出节点只有一条流向算子的连接）
        const outgoingLinks = graph.getConnectedLinks(currentNode, {
            outbound: true
        });

        // 遍历并添加所有下游节点
        outgoingLinks.forEach(link => {
            const nextNode = link.getTargetElement();
            if (nextNode) {
                queue.push(nextNode);
            }
        });
    }

    return false;
};

/**
 * 检测两个格式数组是否有交集
 * @param {string[]} arr1 格式数组1
 * @param {string[]} arr2 格式数组2
 * @returns 
 */
const hasFormatIntersection = (arr1, arr2) => {
    return arr1.some(item => arr2.includes(item));
};

// 重构的metadata获取方法
const fetchOperatorMetadata = async (operatorIdentifier) => {
    try {
        const response = await axios.get(`/api/processes/${operatorIdentifier}`);
        if (response.data.success) {
            const data = response.data.data;

            // 提取输入的ComplexData格式
            const inputFormats = [];
            data.Input?.forEach(inputParam => {
                inputParam.ComplexData?.Format?.forEach(format => {
                    inputFormats.push(format.mimeType);
                });
            });
            const uniqueInputFormats = [...new Set(inputFormats)];

            // 提取每个输出的格式列表
            const outputFormatsList = [];
            data.Output?.forEach(outputParam => {
                const formats = outputParam.ComplexData?.Format?.map(f => f.mimeType) || [];
                outputFormatsList.push(formats);
            });

            // 返回时包含原始输入参数
            return {
                inputParams: data.Input || [],  // 关键修复：添加 Input 的原始数据
                inputFormats: uniqueInputFormats,
                outputs: data.Output || [],
                outputFormatsList
            };
        } else {
            return { inputParams: [], inputFormats: [], outputs: [], outputFormatsList: [] };
        }
    } catch (error) {
        return { inputParams: [], inputFormats: [], outputs: [], outputFormatsList: [] };
    }
};

// 拖拽开始事件
const onDragStart = (operator, event) => {
    if (tool.value === 'select') {
        event.dataTransfer.setData("operator", JSON.stringify(operator));  // 允许拖拽时设置数据
        // console.log("Dragging operator:", operator.Identifier);  // 可以调试输出拖拽的算子
    } else {
        event.preventDefault();  // 如果不是选择工具，阻止默认拖拽行为
    }
};
// onDrop函数：拖拽释放
const onDrop = (event) => {
    if (tool.value === 'select') {
        const operator = JSON.parse(event.dataTransfer.getData("operator"));
        const { offsetX, offsetY } = event;

        const operatorNode = createOperatorNode(operator, offsetX, offsetY);

        fetchOperatorMetadata(operator.Identifier).then(({
            inputFormats,
            outputs,
            outputFormatsList
        }) => {
            // 设置算子的输入格式列表
            operatorNode.set('inputSupportedFormats', inputFormats);

            outputs.forEach((output, index) => {
                const outputNode = new joint.shapes.standard.Ellipse();
                // 获取当前输出的格式列表
                const supportedFormats = outputFormatsList[index] || [];

                // 设置输出节点元数据
                outputNode.set({
                    parentOperatorId: operatorNode.id,
                    nodeType: 'output',
                    supportedFormats  // 存储所有支持的格式
                });

                // 设置悬停提示
                outputNode.attr('title', `支持格式: ${supportedFormats.join(', ') || '无'}`);

                // 布局和样式保持不变...
                outputNode.position(offsetX + operatorNode.get('size').width + 100, offsetY + (index * 60));
                outputNode.resize(80, 40);
                outputNode.attr({
                    body: { fill: "lightgreen" },
                    label: { text: output.Identifier, fill: "black" }
                });

                // 连接线保持不变...
                const link = new joint.shapes.standard.Link({
                    source: operatorNode,
                    target: outputNode,
                    attrs: { line: { stroke: 'red', strokeWidth: 2 } }
                });

                // 修正为通过全局Paper实例访问
                getGlobalPaper().model.addCells([outputNode, link]); // ✅
            });
        });
    }
};

const setTool = (toolName) => {
    // const currentPaper = paperRef.value;
    const currentPaper = getGlobalPaper(); // [!code focus] 
    if (!currentPaper || !currentPaper.el) {
        console.error("Paper is not initialized properly.");
        return;
    }

    // Remove all existing event listeners
    currentPaper.off('element:pointerclick');
    currentPaper.off('blank:pointerclick');

    // tool.value = toolName;
    switch (toolName) {
        case 'select':
            currentPaper.options.interactive = { elementMove: true };
            currentPaper.el.style.cursor = 'grab';

            // 新增：监听算子节点点击事件（需要保持event参数）
            currentPaper.on('element:pointerclick', (elementView, event) => {
                const model = elementView.model;
                if (model.get('nodeType') === 'operator') {
                    // 防止在连接模式下触发跳转
                    if (tool.value !== 'connect') {
                        handleOperatorClick(model);
                    }
                }
            });
            break;
        case 'connect':
            currentPaper.options.interactive = { elementMove: false };
            currentPaper.el.style.cursor = 'crosshair';
            connectionSource.value = null; // 重置连接源

            currentPaper.on('element:pointerclick', (elementView, event) => {
                const elementModel = elementView.model;

                if (!connectionSource.value) {
                    // --------------------------- 规则1：源节点必须是输出节点 -----------------------------
                    if (elementModel.get('nodeType') !== 'output') {
                        ElMessage.warning('只能从输出节点（椭圆形）发起连接');
                        return;
                    }
                    connectionSource.value = elementModel;
                    elementView.highlight();

                } else {
                    const sourceNode = connectionSource.value;
                    const targetNode = elementModel;

                    // ----------------------------- 规则2：禁止自连接 ---------------------------------
                    if (sourceNode === targetNode) {
                        ElMessage.warning('不允许节点连接到自身');
                        currentPaper.findViewByModel(sourceNode).unhighlight();
                        connectionSource.value = null;
                        return;
                    }

                    // ------------------- 规则3：目标节点必须是算子节点（矩形） ------------------------
                    if (targetNode.get('nodeType') !== 'operator') {
                        ElMessage.warning('只能连接到输入节点（矩形）');
                        currentPaper.findViewByModel(sourceNode).unhighlight();
                        connectionSource.value = null;
                        return;
                    }

                    // ----------- 规则4（可选）：同一源输出节点不允许重复连接到同一目标算子 --------------
                    const existingLinks = currentPaper.model.getLinks().filter(link => {
                        return link.source().id === sourceNode.id && link.target().id === targetNode.id;
                    });
                    if (existingLinks.length > 0) {
                        ElMessage.warning('已有相同连接');
                        currentPaper.findViewByModel(sourceNode).unhighlight();
                        connectionSource.value = null;
                        return;
                    }

                    // ----------------- 规则5（可选）：禁止输出节点连接到父算子 ------------------------
                    if (sourceNode.get('nodeType') === 'output' && targetNode.get('nodeType') === 'operator') {
                        if (sourceNode.get('parentOperatorId') === targetNode.id) {
                            ElMessage.warning('子节点不能逆向连接父节点');
                            currentPaper.findViewByModel(sourceNode).unhighlight();
                            connectionSource.value = null;
                            return;
                        }
                    }

                    // -----------------------新增校验：检查是否会形成闭环 ----------------------------
                    if (targetNode.get('nodeType') === 'operator') {
                        // 获取源输出节点的父算子ID
                        const sourceParentOperatorId = sourceNode.get('parentOperatorId');
                        const sourceParentNode = currentPaper.model.getCell(sourceParentOperatorId);

                        if (isCreatingCycle(currentPaper.model, sourceParentNode, targetNode)) {
                            ElMessage.error('连接将导致闭环，禁止操作');
                            currentPaper.findViewByModel(sourceNode).unhighlight();
                            connectionSource.value = null;
                            return;
                        }
                    }

                    // -----------------------规则6：检查格式兼容性-----------------------
                    // -----------------------规则6：检查格式兼容性-----------------------
                    // 获取源节点支持的格式
                    const sourceFormats = sourceNode.get('supportedFormats') || [];
                    console.log("源节点支持的格式:", sourceFormats);

                    // 获取目标节点支持的格式（这里假设目标算子的所有参数支持的格式一致）
                    const targetFormats = targetNode.get('inputSupportedFormats') || [];
                    console.log("目标节点支持的格式:", targetFormats);

                    // 收集目标节点可用参数（过滤已达最大连接数的参数）
                    const availableParams = Object.entries(targetNode.get('inputParams'))
                        .filter(([paramId, config]) => (
                            config.type === 'ComplexData' &&
                            !/output/gi.test(paramId) &&
                            config.connected < config.maxOccurs
                        ));

                    if (sourceFormats.length === 0 || targetFormats.length === 0) {
                        ElMessage.error(`格式元数据不存在，无法连接`);
                        return cancelConnection();
                    }

                    // 如果只有一个可用参数，则立即检查格式兼容性
                    if (availableParams.length === 1) {
                        if (!hasFormatIntersection(sourceFormats, targetFormats)) {
                            const errorMsg = `格式不兼容！\n输出支持: ${sourceFormats.join(', ') || '无'}\n输入需要: ${targetFormats.join(', ') || '无'}`;
                            ElMessage.error({
                                message: errorMsg,
                                duration: 5000, // 延长显示时间
                                showClose: true
                            });
                            return cancelConnection();
                        }
                    } else {
                        // 如果有多个参数，则进行初步检查，详细检查会在用户选择参数后完成
                        if (!hasFormatIntersection(sourceFormats, targetFormats)) {
                            const errorMsg = `格式不兼容（初步检查失败）！\n输出支持: ${sourceFormats.join(', ') || '无'}\n输入需要: ${targetFormats.join(', ') || '无'}`;
                            ElMessage.error({
                                message: errorMsg,
                                duration: 5000,
                                showClose: true
                            });
                            return cancelConnection();
                        }
                    }


                    // ----------------------- 新增：验证目标算子的参数限制 -----------------------
                    if (targetNode.get('nodeType') === 'operator') {
                        const inputParams = targetNode.get('inputParams') || {};

                        // ------------------------------------------------------------------------------
                        // 关键修改：使用正则表达式过滤掉名称含 output 的参数（不区分大小写）
                        // ------------------------------------------------------------------------------
                        const complexParams = Object.entries(inputParams)
                            .filter(([paramId, config]) => {
                                return (
                                    config.type === 'ComplexData' &&
                                    !/output/gi.test(paramId) // 排除 paramId中含 "output"（不区分大小写）
                                );
                            });

                        if (complexParams.length === 0) {
                            ElMessage.error('目标算子无可用ComplexData参数');
                            return cancelConnection();
                        }

                        // ----- 打印参数信息到控制台（已过滤无效参数） -----
                        console.log('目标算子参数列表:');
                        complexParams.forEach(([paramId, config]) => {
                            console.log(`
                                参数标识: ${paramId}
                                类型: ${config.type}
                                最小出现数: ${config.minOccurs}
                                最大出现数: ${config.maxOccurs}
                                当前连接数: ${config.connected}
                            `);
                        });

                    }

                    // 收集目标节点可用参数（过滤已达最大连接数的参数）
                    // const availableParams = Object.entries(targetNode.get('inputParams'))
                    //     .filter(([paramId, config]) => (
                    //         config.type === 'ComplexData' &&
                    //         !/output/gi.test(paramId) &&
                    //         config.connected < config.maxOccurs
                    //     ));

                    if (availableParams.length === 0) {
                        ElMessage.error('目标参数已达最大连接数');
                        return cancelConnection();
                    }

                    if (availableParams.length === 1) {
                        finalizeConnection(availableParams[0][0], sourceNode, targetNode);
                    } else {
                        pendingConnection.value = { sourceNode, targetNode };
                        // 关键修复：传入正确的参数
                        showParamListPopupByMouse(
                            event.clientX,
                            event.clientY,
                            targetNode.get('inputParams')
                        );
                    }
                    // currentPaper.model.addCell(link);
                    // 重置状态
                    currentPaper.findViewByModel(sourceNode).unhighlight();
                    connectionSource.value = null;
                }
            });


            // 点击空白处取消连接
            currentPaper.on('blank:pointerclick', () => {
                if (connectionSource.value) {
                    currentPaper.findViewByModel(connectionSource.value).unhighlight();
                    connectionSource.value = null;
                }
            });
            break;
        case 'delete':
            currentPaper.options.interactive = { elementMove: false, linkMove: false };
            currentPaper.el.style.cursor = 'not-allowed';
            currentPaper.on('element:pointerclick', (elementView) => {
                elementView.model.remove();
            });
            break;
        case 'save':
            const workflowId = route.params.workflowId;

            // 获取 JointJS 画布上的所有节点
            const paper = getGlobalPaper();
            if (!paper?.model) {
                ElMessage.error('画布未正确初始化');
                return;
            }

            const allCells = paper.model.getCells();
            const workflowNodes = [];
            const workflowLinks = [];

            allCells.forEach(cell => {
                if (cell.get('nodeType') === 'operator') {
                    // 根据 operatorIdentifier 获取 Vuex 中保存的完整算子配置
                    const operatorIdentifier = cell.get('operatorIdentifier');
                    const operatorConfig = store.getters['workflow/getOperatorConfigByIdentifier'](operatorIdentifier);
                    if (operatorConfig) {
                        // 合并节点 id 和 Vuex 中完整的配置
                        workflowNodes.push({
                            ...operatorConfig,
                            id: cell.id // 用 JointJS 节点的 id 替换（或保留）原来的 id
                        });
                    } else {
                        // 如果未找到配置，则使用节点的现有 inputParams（不推荐）
                        workflowNodes.push({
                            id: cell.id,
                            identifier: operatorIdentifier,
                            inputParams: cell.get('inputParams'),
                            outputParams: cell.get('outputParams'),
                            executionMode: 'async'
                        });
                    }
                } else if (cell.isLink()) {
                    const sourceId = cell.get('source')?.id;
                    const targetId = cell.get('target')?.id;
                    const paramId = cell.get('params')?.targetParam;
                    if (sourceId && targetId && paramId) {
                        workflowLinks.push({ sourceId, targetId, paramId });
                    }
                }
            });

            // 可选：如果需要将最新的节点与连接信息存入 Vuex，也可以调用下面的 dispatch
            store.dispatch('workflow/saveOperatorConfig', workflowNodes);
            store.dispatch('workflow/saveWorkflowLinks', workflowLinks);

            if (workflowNodes.length === 0) {
                ElMessage.warning('工作流节点为空，无法保存');
                return;
            }

            // 构造完整的 JSON 结构
            const workflowJSON = JSON.stringify({
                workflowId,
                nodes: workflowNodes,
                links: workflowLinks
            }, null, 2);

            console.log("最终保存的工作流结构:", workflowJSON);

            // 发送到后端（示例）
            axios.post('/api/saveWorkflow', { data: workflowJSON })
                .then(() => {
                    ElMessage.success('工作流保存成功！');
                })
                .catch(error => {
                    console.error("保存失败:", error);
                    ElMessage.error('保存失败，请检查控制台');
                });
            break;

        default:
            currentPaper.options.interactive = true;
            currentPaper.el.style.cursor = 'default';
    }
};


// 创建算子节点和对应的输出节点
const createOperatorNode = (operator, offsetX, offsetY) => {
    const paper = getGlobalPaper();
    if (!paper?.model) throw new Error("模型未初始化");

    // 计算算子节点宽度
    const textWidth = operator.Identifier.length * 8;
    const minWidth = 100;
    const width = Math.max(minWidth, textWidth + 20);

    // 创建算子矩形节点
    const operatorNode = new joint.shapes.standard.Rectangle();
    operatorNode.position(offsetX, offsetY);
    operatorNode.resize(width, 40);
    operatorNode.attr({
        body: { fill: "lightblue" },
        label: { text: operator.Identifier, fill: "black" },
    });

    operatorNode.set('nodeType', 'operator');
    operatorNode.set('operatorIdentifier', operator.Identifier);
    operatorNode.set('label', { text: operator.Identifier });

    // 初始化输入参数
    operatorNode.set('inputParams', {});

    // 将节点添加到 JointJS 画布
    paper.model.addCell(operatorNode);

    // 异步获取元数据并存储到 Vuex
    fetchOperatorMetadata(operator.Identifier).then((metadata) => {
        const inputParams = {};
        metadata.inputParams?.forEach(param => {
            if (param.DataType === 'ComplexData') {
                inputParams[param.Identifier] = {
                    type: 'ComplexData',
                    minOccurs: param.minOccurs,
                    maxOccurs: param.maxOccurs,
                    connected: 0,
                    supportedFormats: param.ComplexData?.Format?.map(f => f.mimeType) || []
                };
            }
        });

        operatorNode.set('inputParams', inputParams);
        console.log(`算子参数配置:`, inputParams);

        // 存储节点信息到 Vuex
        store.dispatch('workflow/saveOperatorConfig', {
            id: operatorNode.id,
            identifier: operator.Identifier,
            inputParams
        });
    });

    return operatorNode;
};



// 显示参数弹窗（由节点点击触发）
const showParamListPopupByMouse = (clientX, clientY, params) => {
    // 计算包含滚动偏移的绝对坐标
    const scrollX = window.scrollX || window.pageXOffset;
    const scrollY = window.scrollY || window.pageYOffset;
    console.log("scrollX, scrollY");
    console.log(scrollX, scrollY);

    popupPosition.value = {
        x: clientX + scrollX,
        y: clientY + scrollY + 30
    };

    currentParams.value = Object.entries(params)
        .filter(([paramId, config]) =>
            config.type === 'ComplexData' &&
            !/output/gi.test(paramId)
        )
        .map(([id, config]) => ({
            id,
            connected: config.connected,
            max: config.maxOccurs
        }));

    showParams.value = true;
};
// 点击空白处关闭弹窗
const onClickOutside = () => {
    showParams.value = false;
};

// 新增处理方法
const handleParamSelected = (paramId) => {
    if (!pendingConnection.value) return;

    const { sourceNode, targetNode } = pendingConnection.value;

    // 获取源节点支持的格式
    const sourceFormats = sourceNode.get('supportedFormats') || [];
    console.log("源节点支持的格式:", sourceFormats);

    // 从目标算子的 inputParams 中获取选中参数的支持格式
    const targetParams = targetNode.get('inputParams') || {};
    const paramConfig = targetParams[paramId];
    const paramFormats = paramConfig && paramConfig.supportedFormats ? paramConfig.supportedFormats : [];
    console.log(`选中的参数 ${paramId} 支持的格式:`, paramFormats);

    // 检查源节点与选中参数的支持格式是否有交集
    if (!hasFormatIntersection(sourceFormats, paramFormats)) {
        const errorMsg = `格式不兼容！\n源节点支持: ${sourceFormats.join(', ') || '无'}\n参数 ${paramId} 支持: ${paramFormats.join(', ') || '无'}`;
        ElMessage.error({
            message: errorMsg,
            duration: 5000,
            showClose: true
        });
        return cancelConnection();
    }

    // 格式兼容则完成连接
    finalizeConnection(paramId, sourceNode, targetNode);

    // 重置状态
    pendingConnection.value = null;
    showParams.value = false;
};


// 完成连接的最终操作
const finalizeConnection = (paramId, sourceNode, targetNode) => {
    const paper = getGlobalPaper();
    if (!paper?.model) {
        ElMessage.error('画布未正确初始化');
        return;
    }

    // 更新目标参数计数
    const params = targetNode.get('inputParams') || {};
    if (params[paramId]) {
        params[paramId].connected += 1;
        targetNode.set('inputParams', { ...params });
    }

    // 创建连线对象
    const link = new joint.shapes.standard.Link({
        source: { id: sourceNode.id },
        target: { id: targetNode.id },
        attrs: {
            line: {
                stroke: '#3c8dbc',
                strokeWidth: 2,
                targetMarker: { name: 'block' }
            }
        },
        params: { targetParam: paramId }
    });

    // 将连线信息存储到 Vuex
    store.dispatch('workflow/saveWorkflowLinks', {
        sourceId: sourceNode.id,
        targetId: targetNode.id,
        paramId
    });

    // 添加连线到 JointJS 画布
    paper.model.addCell(link);
};


</script>

<style scoped>
.operator-workflow {
    display: flex;
    justify-content: space-between;
    /* 左右两侧区域分开，右侧靠右 */
}


/* 左边区域：工具栏 + 画布 */
.left-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    flex-grow: 1;
    /* 确保占满剩余空间 */
    flex-shrink: 0;
    /* 防止收缩 */
}


/* 工具栏样式 */
.toolbar-container {
    padding: 3px 10px;
    background-color: #000000;
    border-bottom: 1px solid #ddd;
    z-index: 1;
    width: 1470px;
}

/* 主内容部分（画布） */
.content-container {
    flex: 1;
    /* 让内容区域自动填充剩余空间 */
    background-color: #000000;
    display: flex;
    position: relative;
    overflow: auto;
    height: 100%;
    /* 使用相对高度继承父容器 */
    margin-top: 8px;
    /* 添加间距防止顶栏遮挡 */
    min-height: 1000px;
    /* 保证最小可视区域 */
}

/* 右侧区域：工具箱 */
.toolbox-container {
    padding: 20px;
    height: calc(100vh - 100px);
    overflow-y: auto;
    width: 320px;
    position: relative;
    border-left: 1px solid #2d2d2d;
    justify-self: flex-end;
    /* 确保工具箱区域靠右 */
}

/* 搜索框样式 */
.search-box {
    --el-input-bg-color: #2d2d2d;
    --el-input-text-color: #e0e0e0;
    --el-input-border-color: #444;
    --el-input-icon-color: #e0e0e0;
    margin-bottom: 16px;
}

.search-box:hover {
    --el-input-border-color: #666;
}

.search-box:focus-within {
    --el-input-border-color: #409eff;
}

.joint-element.operator-node {
    cursor: pointer;
    transition: filter 0.2s;
}

.joint-element.operator-node:hover {
    filter: brightness(1.1);
    box-shadow: 0 0 8px rgba(0, 0, 0, 0.2);
}
</style>
