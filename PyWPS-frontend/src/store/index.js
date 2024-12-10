import {createStore} from 'vuex';
import operator from './operator'; // 算子模块
import knowledgeGraph from './knowledge-graph'; // 知识图谱模块
import fileManagement from './file-management'; // 文件管理模块


const store = createStore({
    modules: {
        operator,
        knowledgeGraph,
        fileManagement,
    },
});

export default store;
