import mimetypes


# 添加常用的GIS文件格式
def add_mimetypes():
	mimetypes.add_type("x-world/x-vrt", ".vrt")
	mimetypes.add_type('application/x-shapefile', '.shp')
	mimetypes.add_type('application/vnd.geo+json', '.geojson')
	mimetypes.add_type('application/vnd.google-earth.kml+xml', '.kml')
	mimetypes.add_type('application/vnd.google-earth.kmz', '.kmz')
	mimetypes.add_type('application/gpx+xml', '.gpx')
	mimetypes.add_type('image/tiff', '.tif')
	mimetypes.add_type('image/tiff', '.tiff')
	mimetypes.add_type('application/x-esri-grid', '.asc')
	mimetypes.add_type('application/x-hdf', '.hdf')
	mimetypes.add_type('application/x-netcdf', '.nc')
	mimetypes.add_type('application/x-erdas-imagine', '.img')
	mimetypes.add_type('application/x-grass-ascii-raster', '.asc')
	mimetypes.add_type('application/x-arcinfo-binary-coverage', '.adf')
	mimetypes.add_type('application/x-protobuf', '.mvt')
	mimetypes.add_type('application/x-shp-xml', '.shp.xml')
	mimetypes.add_type('application/x-sdat', '.sdat')
