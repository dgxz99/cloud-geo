// src/store/operator.js
const state = {
    operators: [],
    loading: false,
    selectedOperator: null, // 选中算子
    processedData: [] // 改为数组
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
        state.processedData.push(data); // 动态添加新结果
    },
    // mutations
    ADD_TASK(state, task) {
        state.processedData.push(task);
    },
    UPDATE_TASK_STATUS(state, {taskId, status, errorMessage = null, completionTime = null, output = null}) {
        const taskIndex = state.processedData.findIndex(t => t.jobId === taskId);
        if (taskIndex !== -1) {
            const updatedTask = {
                ...state.processedData[taskIndex],
                status,
                errorMessage,
                completionTime,
                output, // 更新 output 数据
            };
            state.processedData.splice(taskIndex, 1, updatedTask);
        }
    }


};

const actions = {
    async fetchOperators({commit}) {
        commit('setLoading', true);
        try {
            const response = await fetch('/api/processes?service=WPS');
            const data = await response.json();
            console.log("Fetched operators data:", data);

            // 提取算子列表
            const operators = data.contents || [];
            commit('setOperators', operators);
        } catch (error) {
            console.error("Failed to fetch operators:", error);
        } finally {
            commit('setLoading', false);
        }
    },
};

export default {
    namespaced: true,
    state,
    mutations,
    actions,
};
