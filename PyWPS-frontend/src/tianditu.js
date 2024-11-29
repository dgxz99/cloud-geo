import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

export function initializeTianditu(container) { // 接收 map 容器
    let map = L.map(container, {
        minZoom: 3,
        maxZoom: 18,
        center: L.latLng(33.89945, 103.40769),
        zoom: 5,
        zoomControl: false,
        attributionControl: false,
    });

    const createTileLayer = (layer, subLayer) => {
        return L.tileLayer(`http://t{s}.tianditu.gov.cn/${layer}_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=${subLayer}&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TileMatrix={z}&TileRow={y}&TileCol={x}&tk=a9ddfcb66bcde64828a714ef5d4456e3`, {
            subdomains: ['0', '1', '2', '3', '4', '5', '6', '7'],
            tileSize: 256,
            minZoom: 3,
            maxZoom: 18,
        });
    };

    // Tianditu Layers
    const vecLayer = createTileLayer('vec', 'vec');
    const imgLayer = createTileLayer('img', 'img');
    const terLayer = createTileLayer('ter', 'ter');
    const vecAnnotationLayer = createTileLayer('cva', 'cva');
    const imgAnnotationLayer = createTileLayer('cia', 'cia');
    const terAnnotationLayer = createTileLayer('cta', 'cta');

    // OSM Layer with English Labels
    const osmLayer = L.tileLayer('https://tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png', {
        subdomains: ['a', 'b', 'c'],
        tileSize: 256,
        minZoom: 3,
        maxZoom: 18,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });



    // const baseLayers = {
    //     "OSM 地图": osmLayer,
    //     "矢量图": vecLayer,
    //     "影像图": imgLayer,
    //     "地形图": terLayer,
    // };
    //
    // const overlayLayers = {
    //     "矢量注记": vecAnnotationLayer,
    //     "影像注记": imgAnnotationLayer,
    //     "地形注记": terAnnotationLayer,
    // };

    // Base layers to switch between
    const baseLayers = {
        "OSM Map": osmLayer, // OSM 地图
        "Vector Map": vecLayer, // Tianditu 矢量图
        "Satellite Imagery": imgLayer, // Tianditu 影像图
        "Topographic Map": terLayer, // Tianditu 地形图
    };

    const overlayLayers = {
        "Vector Annotations": vecAnnotationLayer, // 矢量注记
        "Satellite Annotations": imgAnnotationLayer, // 影像注记
        "Topographic Annotations": terAnnotationLayer, // 地形注记
    };

    // Add the layers control to the map
    L.control.layers(baseLayers, overlayLayers).addTo(map);
    osmLayer.addTo(map); // 默认加载 Leaflet OSM 图层

    return map;
}
