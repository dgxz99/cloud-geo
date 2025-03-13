<template>
    <div id="cesiumContainer"></div>
</template>

<script>
import {onMounted} from 'vue';
import {Ion, Viewer} from 'cesium';
import 'cesium/Build/Cesium/Widgets/widgets.css';

Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJiZjI2ZjBlZi0yNWI3LTRhOWQtODI5NS03YjJkYzc5ZGUwN2YiLCJpZCI6MjI4MTk2LCJpYXQiOjE3MzY0MDMwODB9.GEvgz5GsoBpWQQCyVKL7B3Tx4a9Kk5Omz4rZo4Z_X_U'

export default {
    name: 'App',
    setup() {
        onMounted(() => {
            const viewer = new Viewer('cesiumContainer', {
                animation: true, //是否打开创建动画小控件，即左下角的仪表
                baseLayerPicker: true,//是否显示图层选择器
                fullscreenButton: true,//是否显示全屏按钮
                geocoder: true,//是否显示Geocoder(右上角的查询按钮)
                homeButton: true,//是否显示Home按钮
                infoBox: true,//是否显示信息框
                sceneModePicker: true,//是否显示三维地球/二维地图选择器
                selectionIndicator: true,//是否显示选取指示器
                timeline: true, //是否关闭时间线
                navigationHelpButton: false, // 帮助提示
            });
            // 去除版权信息
            viewer._cesiumWidget._creditContainer.style.display = 'none';
        })
    }
}
</script>

<style scoped>
#cesiumContainer {
    height: 100%;
    margin: 0;
    padding: 0;
}

</style>