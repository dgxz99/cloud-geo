// src/store/operator.js
const state = {
    operators: [],
    loading: false,
    selectedOperator: null, // 选中算子
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
};

const actions = {
    async fetchOperators({ commit }) {
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
