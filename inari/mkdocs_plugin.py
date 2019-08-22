try:
    import mkdocs
except ImportError:
    mkdocs = None

if mkdocs:

    class Plugin(mkdocs.plugins.BasePlugin):
        pass
