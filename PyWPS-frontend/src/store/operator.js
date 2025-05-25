// src/store/operator.js
const state = {
    operators: [],
    loading: false,
    selectedOperator: null, // 选中算子
    processedData: [], // 改为数组
    workflow: {
        nodes: [], // 节点列表
        edges: [], // 边列表
        zoomLevel: 1.0, // 当前缩放级别
        panOffset: { x: 0, y: 0 }, // 平移偏移量
        selectedNode: null, // 当前选中节点
        selectedEdge: null // 当前选中边
    },
    workflowGraphData: null // 新增

};

const mutations = {
    setOperators(state, operators) {
        state.operators = operators;
    },
    setSelectedOperator(state, operator) {
        state.selectedOperator = operator;
    },
    setLoading(state, loading) {
        state.loading = loading;
    },
    setProcessedData(state, data) {
        state.processedData.push(data);
    },
    ADD_TASK(state, task) {
        state.processedData.push(task);
    },
    UPDATE_TASK_STATUS(state, { taskId, status, errorMessage = null, completionTime = null, output = null }) {
        const taskIndex = state.processedData.findIndex(t => t.jobId === taskId);
        if (taskIndex !== -1) {
            const updatedTask = {
                ...state.processedData[taskIndex],
                status,
                errorMessage,
                completionTime,
                output,
            };
            state.processedData.splice(taskIndex, 1, updatedTask);
        }
    },
    // 工作流相关mutations
    ADD_NODE(state, node) {
        state.workflow.nodes.push(node);
    },
    REMOVE_NODE(state, nodeId) {
        state.workflow.nodes = state.workflow.nodes.filter(n => n.id !== nodeId);
    },
    ADD_EDGE(state, edge) {
        state.workflow.edges.push(edge);
    },
    REMOVE_EDGE(state, edgeId) {
        state.workflow.edges = state.workflow.edges.filter(e => e.id !== edgeId);
    },
    UPDATE_ZOOM(state, zoomLevel) {
        state.workflow.zoomLevel = zoomLevel;
    },
    UPDATE_PAN(state, offset) {
        state.workflow.panOffset = offset;
    },
    SELECT_NODE(state, node) {
        state.workflow.selectedNode = node;
    },
    SELECT_EDGE(state, edge) {
        state.workflow.selectedEdge = edge;
    },

    // 新增mutation以缓存算子数据
    ADD_OPERATOR(state, operator) {
        const exists = state.operators.some(
            op => op.Identifier.toLowerCase() === operator.Identifier.toLowerCase()
        )
        if (!exists) {
            state.operators.push(operator)
        }
    },

    // 保存工作流状态
    SAVE_WORKFLOW(state, graphData) {
        state.workflowGraphData = graphData;
    },
    // 清除工作流状态
    CLEAR_WORKFLOW(state) {
        state.workflowGraphData = null;
    }
};

const actions = {
    // actions 中的 fetchOperators 方法
    async fetchOperators({ commit }) {
        commit('setLoading', true);
        try {
            const response = await fetch('/processes?service=WPS')

            // 校验 HTTP 状态码
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)

            const data = await response.json()

            // 深层数据校验
            const operators = data?.data?.contents
                ? JSON.parse(JSON.stringify(data.data.contents))
                : []

            commit('setOperators', operators)
        } catch (error) {
            console.error("Operators fetch failed:", error)
            commit('setOperators', []) // 确保有初始值
        } finally {
            commit('setLoading', false)
        }
    },

    // 工作流相关actions
    addNode({ commit }, node) {
        commit('ADD_NODE', node);
    },
    removeNode({ commit }, nodeId) {
        commit('REMOVE_NODE', nodeId);
    },
    addEdge({ commit }, edge) {
        commit('ADD_EDGE', edge);
    },
    removeEdge({ commit }, edgeId) {
        commit('REMOVE_EDGE', edgeId);
    },
    updateZoom({ commit }, zoomLevel) {
        commit('UPDATE_ZOOM', zoomLevel);
    },
    updatePan({ commit }, offset) {
        commit('UPDATE_PAN', offset);
    },
    selectNode({ commit }, node) {
        commit('SELECT_NODE', node);
    },
    selectEdge({ commit }, edge) {
        commit('SELECT_EDGE', edge);
    },
    saveWorkflow({ state }) {
        // 保存工作流到本地存储
        localStorage.setItem('workflow', JSON.stringify(state.workflow));
    },
    loadWorkflow({ commit }) {
        // 从本地存储加载工作流
        const workflow = JSON.parse(localStorage.getItem('workflow') || '{}');
        if (workflow.nodes) {
            commit('ADD_NODE', workflow.nodes);
        }
        if (workflow.edges) {
            commit('ADD_EDGE', workflow.edges);
        }
    }
};


const getters = {
    // 根据算子标识符获取完整算子信息
    getOperatorById: (state) => (identifier) => {
        return state.operators.find(
            op => op.Identifier.toLowerCase() === identifier.toLowerCase()
        )
    },

    // 其他可选getter...
}



export default {
    namespaced: true,
    getters,
    state,
    mutations,
    actions,
};
