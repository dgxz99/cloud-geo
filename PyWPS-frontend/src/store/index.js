// src/store/index.js
import {createStore} from 'vuex';
import operator from './operator'; // 引入算子数据模块
import knowledgeGraph from './knowledge-graph'; // 引入知识图谱数据模块
import {fileManagement} from './fileManagement'; // 引入文件管理模块

// 创建 Vuex store
const store = createStore({
    modules: {
        operator,
        knowledgeGraph,
        fileManagement,  // 添加文件管理模块
    },
});

// 导出 store
export default store;
