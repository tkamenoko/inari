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
def on_config(self, config, **kw)
```


------

[**on_pre_build**](#Plugin.on_pre_build){: #Plugin.on_pre_build }

```python
def on_pre_build(self, config, **kw)
```


------

[**on_serve**](#Plugin.on_serve){: #Plugin.on_serve }

```python
def on_serve(self, server, config, builder, **kw)
```
