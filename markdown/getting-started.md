# Getting Started

## Install

```shell
pip install inari
```

## Use CLI

```shell
inari <module-name> <out-dir> [-n <out-name>]
```

* `module-name` : Target module to make documents.
* `out-dir` : Directory to put documents.
* `out-name` : Top level directory/file name. `module-name` is used by default.

## Use MkDocs Plugin

First, install with [MkDocs](https://www.mkdocs.org/) .

```shell
pip install inari[mkdocs]
```

Initialize project.

```shell
mkdocs new my-project
cd my-project
```

Then, fix `mkdocs.yml` .

```yaml
site_name: My Docs

docs_dir: "docs" # same as default

plugins:
    - search # MkDocs default plugin
    - inari:
        module: <module-name> # required
        out-name: api # optional. Default: <module-name>
        # no `out-dir` option because `inari` uses `docs_dir` in the config.

```

After that, running `mkdocs build` will generate your API documents in `docs/api` .
