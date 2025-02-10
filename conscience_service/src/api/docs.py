from ninja.openapi.docs import DocsBase, Swagger, Redoc
from ninja.errors import Http404


class MixedDocs(DocsBase):
    def __init__(self) -> None:
        super().__init__()
        self.swagger = Swagger()
        self.redoc = Redoc()
        self.engines = {
            "swagger": self.swagger,
            "docs": self.redoc,
        }
        self.default_engine = self.redoc

    def render_page(self, request, api, **kwargs):
        engine_name = kwargs.pop("engine", None)
        if engine_name is None:
            engine = self.default_engine
        else:
            engine = self.engines.get(engine_name)

        if engine is None:
            raise Http404(f"Engine {engine_name} not found")

        return engine.render_page(request, api, **kwargs)
