// store/index.js (或你创建store的文件)
import { createStore } from 'vuex';
import operator from './operator';
import knowledgeGraph from './knowledge-graph';
import fileManagement from './file-management';
import workflow from './workflow'; // [!code focus] 新增引入

const store = createStore({
    modules: {
        operator,
        knowledgeGraph,
        fileManagement,
        workflow // [!code focus] 添加至模块列表
    }
});

export default store;
