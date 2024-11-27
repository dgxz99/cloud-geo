// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import MainLayout from '@/views/MainLayout.vue';
import FilesDrawer from '../components/FilesDrawer.vue';
import OperatorToolbox from '../components/OperatorToolbox.vue';
import OperatorOverview from '../components/OperatorOverview.vue';
import KnowledgeGraph from '../components/KnowledgeGraph.vue';
import SearchContainer from '../components/SearchContainer.vue';
import UserContainer from '../components/UserContainer.vue';
import OperatorIdentifier from '@/components/OperatorIdentifier.vue';


const routes = [
    {
        path: '/',
        name: 'MainLayout',
        component: MainLayout,
        meta: { title: '首页' },
        children: [
            {
                path: 'files',
                name: 'Files',
                component: FilesDrawer,
                meta: { title: '导入数据' },
                children: [
                    {
                        path: 'RasterData',
                        name: 'RasterData',
                        component: () => import('../components/RasterData.vue'),
                    },
                    {
                        path: 'VectorData',
                        name: 'VectorData',
                        component: () => import('../components/VectorData.vue'),
                    },
                ]
            },
            {
                path: 'operator-toolbox',
                name: 'OperatorToolbox',
                component: OperatorToolbox,
                meta: { title: '算子工具箱' },
            },
            {
                path: 'operator/:Identifier',
                name: 'OperatorIdentifier',
                component: OperatorIdentifier,
                meta: { title: '算子详情' },
                props: true,
            },
            {
                path: 'operator-overview',
                name: 'OperatorOverview',
                component: OperatorOverview,
                meta: { title: '算子概览' },
            },
            {
                path: 'knowledge-graph',
                name: 'KnowledgeGraph',
                component: KnowledgeGraph,
                meta: { title: '知识图谱' },
            },
            {
                path: 'search',
                name: 'Search',
                component: SearchContainer,
                meta: { title: '搜索' },
            },
            {
                path: 'user',
                name: 'User',
                component: UserContainer,
                meta: { title: '用户' },
            },
        ]
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

//后置路由守卫
// 路由守卫，用于在每次路由变化前设置页面标题
router.beforeEach((to, from, next) => {
    document.title = to.meta.title || '默认标题';
    next();
});

export default router;