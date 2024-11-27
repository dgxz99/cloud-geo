// src/store/index.js
import { createStore } from 'vuex';
import operator from './operator'; // 引入算子数据模块
import knowledgeGraph from './knowledge-graph'; // 引入知识图谱数据模块

// 创建 Vuex store
const store = createStore({
    modules: {
        operator,
        knowledgeGraph,
    },
});

// 导出 store
export default store;