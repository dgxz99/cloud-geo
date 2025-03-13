export default {
    namespaced: true,
    state: {
        activeWorkflowId: null,
        workflows: {},
        workflowNodes: [], // 存储工作流节点
        workflowLinks: []  // 存储工作流连接
    },
    mutations: {
        SET_ACTIVE_WORKFLOW(state, workflowId) {
            state.activeWorkflowId = workflowId;
        },
        ADD_OR_UPDATE_OPERATOR_CONFIG(state, { existingConfigIndex, newOperatorConfig }) {
            if (existingConfigIndex !== -1) {
                // 如果已存在相同 identifier，则更新
                state.workflowNodes[existingConfigIndex] = newOperatorConfig;
            } else {
                // 否则新增
                state.workflowNodes.push(newOperatorConfig);
            }
        },
        ADD_WORKFLOW_LINK(state, link) {
            state.workflowLinks.push(link);
        }
    },
    actions: {
        saveOperatorConfig({ commit, state }, payload) {
            // payload 既可以是单个配置，也可以是一个数组（这里根据调用方式自行区分）
            if (Array.isArray(payload)) {
                payload.forEach(item => {
                    let index = state.workflowNodes.findIndex(node => node.identifier === item.identifier);
                    commit('ADD_OR_UPDATE_OPERATOR_CONFIG', { existingConfigIndex: index, newOperatorConfig: item });
                });
            } else {
                commit('ADD_OR_UPDATE_OPERATOR_CONFIG', payload);
            }
        },
        saveWorkflowLinks({ commit }, link) {
            commit('ADD_WORKFLOW_LINK', link);
        }
    },
    getters: {
        currentWorkflow: (state) => state.workflows[state.activeWorkflowId],
        getWorkflowNodes: (state) => state.workflowNodes,
        getWorkflowLinks: (state) => state.workflowLinks,
        // 新增 getter 根据 identifier 获取算子配置
        getOperatorConfigByIdentifier: (state) => (identifier) => {
            return state.workflowNodes.find(node => node.identifier === identifier);
        }
    }
};
