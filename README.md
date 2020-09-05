# Mind Map generator

Small program to generate mind map from YAML notes.
Built upon Graphviz and Pydot

**Features**
- Describe your map in readable, clean and minimalistic YAML
- Use themes to apply common attributes to nodes without boilerplate dot files
- Use Python expressions and regexps as predicates to apply styles dinamically

## Usage

```shell
Usage: mind-mapper [OPTIONS] MAP_PATH OUTPUT_PATH

  Render Mind Map from YAML description with given theme.

Options:
  -t, --theme TEXT    Built-in theme name or theme file path  [default:
                      mind_mapper.themes.default]

  -p, --program TEXT  Graphviz rendering program  [default: dot]
  -f, --format TEXT   [default: png]
  -v                  Enable debug logging
  --help              Show this message and exit.

```
