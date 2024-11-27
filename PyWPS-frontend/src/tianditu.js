import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

export function initializeTianditu() {
    let map = L.map("MapContainer", {
        minZoom: 3,
        maxZoom: 18,
        center: L.latLng(33.89945, 103.40769),
        zoom: 5,
        zoomControl: false,
        attributionControl: false,
    });

    // 通用的函数，用于创建天地图图层
    const createTileLayer = (layer, subLayer) => {
        return L.tileLayer(`http://t{s}.tianditu.gov.cn/${layer}_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=${subLayer}&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TileMatrix={z}&TileRow={y}&TileCol={x}&tk=a9ddfcb66bcde64828a714ef5d4456e3`, {
            subdomains: ['0', '1', '2', '3', '4', '5', '6', '7'],
            tileSize: 256,
            minZoom: 3,
            maxZoom: 18,
        });
    };

    // 创建各个基础图层
    const vecLayer = createTileLayer('vec', 'vec');
    const imgLayer = createTileLayer('img', 'img');
    const terLayer = createTileLayer('ter', 'ter');

    // 创建各个注记图层
    const vecAnnotationLayer = createTileLayer('cva', 'cva');
    const imgAnnotationLayer = createTileLayer('cia', 'cia');
    const terAnnotationLayer = createTileLayer('cta', 'cta');

    // 创建图层控制控件，并添加到地图
    const baseLayers = {
        "矢量图": vecLayer,
        "影像图": imgLayer,
        "地形图": terLayer,
    };

    const overlayLayers = {
        "矢量注记": vecAnnotationLayer,
        "影像注记": imgAnnotationLayer,
        "地形注记": terAnnotationLayer,
    };

    L.control.layers(baseLayers, overlayLayers).addTo(map);

    // 默认显示矢量图层和矢量注记图层
    imgLayer.addTo(map);
    imgAnnotationLayer.addTo(map);

    return map;
}
