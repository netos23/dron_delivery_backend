from django.urls import path, include


def add_module_urls(module_name: str, urlpatterns: list):
    """Extend root urlpatterns from module.urls.urlpatterns"""
    module = __import__(module_name)
    if getattr(module, "urls"):
        url_path = f"{module_name}.urls"
        urlpatterns.append(path(f"{module_name}/", include(url_path)))
