from .pywps_api import pywps_blue
from .health_api import health_blue
from .file_api import file_blue
from .provenance_api import provenance_blue

DEFAULT_BLUEPRINT = [pywps_blue, file_blue, provenance_blue, health_blue]


def config_blueprint(app):
    for blueprint in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint)
