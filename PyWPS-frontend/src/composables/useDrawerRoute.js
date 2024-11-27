import { ref, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export function useDrawerRoute(routePath = '/files') {
    const isDrawerVisible = ref(false)
    const route = useRoute()
    const router = useRouter()

    // 切换弹窗显示状态
    const toggleDrawer = () => {
        isDrawerVisible.value = !isDrawerVisible.value
        router.push({ path: isDrawerVisible.value ? routePath : '/' })
    }

    // 监听路由变化来控制弹窗显示
    watch(route, (newRoute) => {
        isDrawerVisible.value = newRoute.path === routePath
    })

    // 页面加载时根据路径决定弹窗是否显示
    onMounted(() => {
        isDrawerVisible.value = route.path === routePath
    })

    return {
        isDrawerVisible,
        toggleDrawer
    }
}