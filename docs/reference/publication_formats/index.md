<!-- docs-type: reference https://diataxis.fr/reference/ -->

# Data formats

OFDS defines schemas based on the [logical data model](../data_model.md) for publishing, storing and exchanging data in the following formats:

```{eval-rst}
.. toctree::
   :maxdepth: 1
   
   json/index.md
   csv
   geopackage/index.md
```

Each format provides containers for publishing one or more networks and options to support pagination and streaming, where appropriate.

When sharing data publicly, to support the widest range of use cases, you should publish your data in as many formats as possible so that users can access data in their preferred format.

```{seealso}
For more information on choosing a data format and on publishing data in multiple formats, see [how to format data for publication](../../guidance/publication.md#how-to-format-data-for-publication).
```
