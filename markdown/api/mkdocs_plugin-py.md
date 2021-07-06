---
module_digest: 6b726e50f73aa227388d65a8d794e4aa
---

# Module inari.mkdocs_plugin


## Classes

### Plugin {: #Plugin }

```python
class Plugin()
```

MkDocs Plugin class.


------

#### Base classes {: #Plugin-bases }

* `mkdocs.BasePlugin`


------

#### Methods {: #Plugin-methods }

[**on_config**](#Plugin.on_config){: #Plugin.on_config }

```python
def on_config(self, config: Config, **kw: Any) -> Config
```


------

[**on_pre_build**](#Plugin.on_pre_build){: #Plugin.on_pre_build }

```python
def on_pre_build(self, config: Config) -> None
```

Build markdown docs from python modules.

------

[**on_serve**](#Plugin.on_serve){: #Plugin.on_serve }

```python
def on_serve(
    self,
    server: LiveReloadServer,
    config: Config,
    builder: Callable[[], None],
    **kw: Any
    ) -> LiveReloadServer
```


------

[**root_module**](#Plugin.root_module){: #Plugin.root_module }

```python
def root_module(self, config: Config) -> ModuleCollector
```
