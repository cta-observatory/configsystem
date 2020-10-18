# Prototyping a config system for ctapipe and other other uses


## Requirements

1. Support deep hierarchies of configurations

  This essentially means that we need to support configuration options
  that are themselves configurable and hand down the necessary config
  to them when a class containing such members is instantiated.

  This makes the configuration a tree.

2. Support lookup by arbitray keys for all config items.

  The simple case is just one global value, but this lookup should work
  on hierachical properties, to support
  * A global default
  * defaults per telescope type / camera type ...
  * value for individual telescope / camera ids

  Where the more fine-grained categories override the coarser values.

  E.g.:

  ```
  cleaning_levels = [
    ('default', 10),
    ('telescope_name', 'LST', 5),
    ('telescope_id', 42, 6),
  ]

  lookup(cleaning_levels) -> 10
  lookup(cleaning_levels, telescope_name='LST', telescope_id=1) -> 5
  lookup(cleaning_levels, telescope_name='MST', telescope_id=10) -> 10
  lookup(cleaning_levels, telescope_name='MST', telescope_id=42) -> 6
  ```

3. Build CLIs for the configurable options automatically


4. Support loading configuration from files

  Most probably at least one (or all) of these should be supported.
  In order of preference:
  * toml
  * yaml
  * json

5. The config system must support the configuration of multiple instances
  of the same class next to each other in the hierarchy (unlike traitlets.config)

6. The system should raise errors for unknown configuration options,
  e.g to prevent unexpected results from simple typing mistakes.

7. It must be possible to configure the type of a variable from a
   list of possible classes or the subclasses.
   E.g. there are several ``ImageExtractors``, so the class used for
   ``CameraCalibrator.image_extractor`` must be configurable through
   the config system.

8. The full config of an object must be accessible / exportable

## Design decisions

* Classes configure their members through configs and kwargs,
  this essentially solves requirement 5.

* The python descriptor protocol is used to define which members of a classed
  are configurable.

* The in-memory representation of the config is a simple dict

* The config tree is build explicitly via the config items that are themselves
  configurable classes.
