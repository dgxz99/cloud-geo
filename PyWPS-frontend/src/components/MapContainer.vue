<template>
    <div id="MapContainer" ref="mapContainer"></div>
</template>

<script>
import {initializeTianditu} from '@/tianditu'; // 天地图初始化工具

export default {
    name: 'MapContainer',
    data() {
        return {
            map: null,  // 用于存储 Leaflet 地图实例
        };
    },
    mounted() {
        // 初始化天地图，并将返回的地图实例赋值给 map 属性
        this.map = initializeTianditu(this.$refs.mapContainer);
        
        
    },
    beforeUnmount() {
        // 组件卸载前销毁地图实例，避免内存泄漏
        if (this.map) {
            this.map.remove();
            this.map = null;
        }
    },
    methods: {
        /**
         * 向地图中添加 GeoJSON 数据
         * @param {Object} geoJsonData - 传入的 GeoJSON 数据
         * @param {boolean} [zoomToData=true] - 是否将视角缩放到数据范围
         * @param {string} [name=''] - 图层的名称
         */
        addGeoJsonToMap(geoJsonData, zoomToData = true, name = '') {
            if (!this.map) return;
            
            // eslint-disable-next-line no-undef
            const geoJsonLayer = L.geoJSON(geoJsonData);
            geoJsonLayer.name = name || `GeoJSON Layer ${Date.now()}`; // 使用传递的文件名作为图层名称
            
            geoJsonLayer.addTo(this.map);
            
            if (zoomToData) {
                this.map.fitBounds(geoJsonLayer.getBounds());
            }
            
            // 触发图层添加的事件，并传递图层信息给父组件
            this.$emit('layer-added', {name: geoJsonLayer.name, layer: geoJsonLayer});
        },
    }
    
}
</script>

<style scoped>
#MapContainer {
    width: 100%;
    height: 100%;
}
</style>