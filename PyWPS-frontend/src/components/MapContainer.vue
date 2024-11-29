<template>
    <div id="MapContainer" ref="mapContainer"></div>
</template>

<script>
import L from 'leaflet';
import { initializeTianditu } from '@/tianditu';

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

            const geoJsonLayer = L.geoJSON(geoJsonData);
            geoJsonLayer.name = name || `GeoJSON Layer ${Date.now()}`; // 使用传递的文件名作为图层名称

            geoJsonLayer.addTo(this.map);

            if (zoomToData) {
                this.map.fitBounds(geoJsonLayer.getBounds());
            }

            // 触发图层添加的事件，并传递图层信息给父组件
            this.$emit('layer-added', { name: geoJsonLayer.name, layer: geoJsonLayer });
        },


        /**
         * 向地图中添加栅格影像图层
         * @param {string} urlTemplate - 栅格图层的 URL 模板
         * @param {string} [name=''] - 图层的名称
         */
        addRasterLayer(urlTemplate, name = '') {
            if (!this.map) return;

            const rasterLayer = L.tileLayer(urlTemplate, {
                subdomains: ['0', '1', '2', '3', '4', '5', '6', '7'],
            });

            rasterLayer.name = name || `Raster Layer ${Date.now()}`; // 使用传递的名称作为图层名称
            rasterLayer.addTo(this.map);

            // 触发图层添加的事件，并传递图层信息给父组件
            this.$emit('layer-added', { name: rasterLayer.name, layer: rasterLayer });
        },

        /**
         * 从地图中移除指定的图层
         * @param {Object} layer - 要移除的图层对象
         */
        removeLayer(layer) {
            if (this.map && layer) {
                this.map.removeLayer(layer);
            }
        }
    }
}
</script>

<style scoped>
#MapContainer {
    width: 100%;
    height: 100%;
}


</style>
