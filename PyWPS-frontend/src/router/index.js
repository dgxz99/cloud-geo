// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import MainLayout from '@/views/MainLayout.vue';
import FilesDrawer from '../components/FilesDrawer.vue';
import OperatorToolbox from '../components/OperatorToolbox.vue';
import OperatorOverview from '../components/OperatorOverview.vue';
import KnowledgeGraph from '../components/KnowledgeGraph.vue';
import SearchContainer from '../components/SearchContainer.vue';
import OperatorIdentifier from '@/components/OperatorIdentifier.vue';


const routes = [
    {
        path: '/',
        name: 'MainLayout',
        component: MainLayout,
        // meta: { title: '首页' },
        children: [
            {
                path: 'files',
                name: 'Files',
                component: FilesDrawer,
                // meta: { title: '导入数据' },
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
                // meta: { title: '算子工具箱' },
            },
            {
                path: 'operator/:Identifier',
                name: 'OperatorIdentifier',
                component: OperatorIdentifier,
                // meta: { title: '算子详情' },
                props: true,
            },
            {
                path: 'operator-overview',
                name: 'OperatorOverview',
                component: OperatorOverview,
                // meta: { title: '算子概览' },
            },
            {
                path: 'knowledge-graph',
                name: 'KnowledgeGraph',
                component: KnowledgeGraph,
                // meta: { title: '知识图谱' },
            },
            {
                path: 'search',
                name: 'Search',
                component: SearchContainer,
                // meta: { title: '搜索' },
            },
            // /
        ]
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

// 路由守卫，用于在每次路由变化前设置页面标题
// router.beforeEach((to, from, next) => {
//     // document.title = to.meta.title || '默认标题';
//     // document.title='CloudGeoPy: 云端地理信息处理平台'
//     // next();
// });

router.beforeEach((to, from, next) => {
    // 标题内容
    // const fullTitle = 'CloudGeoPy: 云端地理信息处理平台';
    const fullTitle = 'CloudGeoPy: Cloud-based Geographic Information Processing Platform';
    let scrollSpeed = 300; // 滚动速度

    // 清除上一个定时器，防止标题滚动重叠
    if (window.titleScrollInterval) {
        clearInterval(window.titleScrollInterval);
    }

    let currentTitle = ''; // 当前显示的标题
    let index = 0; // 滚动起始位置

    // 使用 setInterval 实现标题的滚动效果
    window.titleScrollInterval = setInterval(() => {
        currentTitle = fullTitle.substring(index) + ' ' + fullTitle.substring(0, index);
        document.title = currentTitle; // 更新页签标题
        index = (index + 1) % fullTitle.length; // 循环滚动
    }, scrollSpeed);

    next();
});

// 在页面卸载前清理定时器
window.addEventListener('beforeunload', () => {
    if (window.titleScrollInterval) {
        clearInterval(window.titleScrollInterval);
    }
});

export default router;