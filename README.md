# Prototyping a python configuration system


## Example

```python

from config import Configurable, Int, Float, String, ConfigurableInstance, Path, Lookup


class Cleaning(Configurable):
    pass

class BasicCleaning(Cleaning):
    level = Lookup(Float(5.0), ("type", "id"), help="The cleaning level")

class BetterCleaning(Cleaning):
    level = Lookup(Float(5.0), ("type", "id"), help="The cleaning level")

class ImageProcessor(Configurable):
    cleaning = ConfigurableInstance(Cleaning, default_config=dict(cls=BasicCleaning))


processor = ImageProcessor()

print(processor.cleaning.level["LST", 1]) # => 5.0

processor.cleaning.level = [("type", "LST", 3.0), ("type", "MST", 4.0)]

print(processor.cleaning.level["LST", 1]) # => 3.0
print(processor.cleaning.level["MST", 5]) # => 4.0
```


## Roadmap

* [ ] A good name

* [X] Support deep hierarchies of configurations

    This essentially means that we need to support configuration options
    that are themselves configurable and hand down the necessary config
    to them when a class containing such members is instantiated.

    This makes the configuration a tree.

* [X] Parents must be able to override the default configuration of their
    children. E.g. if `Child` has a configuration item `value` with default `5`,
    A `Parent` with a `child` configuration item has to be able to say that
    the `child.value` default is `10` instead.

* [X] The config system must support the configuration of multiple instances
    of the same class next to each other in the hierarchy (unlike traitlets.config)

* [X] The system should raise errors for unknown configuration options,
    e.g to prevent unexpected results from simple typing mistakes.

* [X] The full config of an object must be accessible / exportable

* [X] It must be possible to configure the type of a variable from a
   list of possible classes or the subclasses.
   E.g. there are several ``ImageExtractors``, so the class used for
   ``CameraCalibrator.image_extractor`` must be configurable through
   the config system.

* [X] Support lookup by arbitray keys for all config items.

    The simple case is just one global value, but the lookup works
    on hierachical properties, to support
    * A global default
    * defaults per telescope type / camera type ...
    * value for individual telescope / camera ids

    Where the more fine-grained categories override the coarser values.

* [ ] Basic set of configuration items with commonly used validators
    * [X] `Int`
    * [X] `Float`
    * [X] `String`
    * [X] `Path`
    * ...

* [ ] Implement container-like configuration items
    * [ ] `List`
    * [ ] `Set`
    * [ ] `Dict`

* [ ] Build CLIs for the configurable options automatically

* [ ] Support loading configuration from files

    Most probably at least one (or all) of these should be supported.
    In order of preference:
    * toml
    * yaml
    * json

    In a sense, this is already supported, since all loaders of these
    formats give you a `dict` and that can be passed as config.

    However, for the CLI use case, we want to be able to pass the config file
    as CLI option and in general we probably also need clever ways to merge
    multiple config files with support for precedence.

## Design decisions

* Classes configure their members through configs and kwargs,
  this essentially solves requirement 5.

* The python descriptor protocol is used to define which members of a classed
  are configurable.

* The in-memory representation of the config is a simple dict

* The config tree is build explicitly via the config items that are themselves
  configurable classes.
