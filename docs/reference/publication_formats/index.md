<!-- docs-type: reference https://diataxis.fr/reference/ -->

# Data formats

```{admonition} 0.3.0 release
Welcome to the Open Fibre Data Standard 0.3.0 release.

We want to hear your feedback on the standard and its documentation. For general feedback, questions and suggestions, you can comment on an existing [discussion](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/discussions) or start a new one. For bug reports or feedback on specific elements of the data model and documentation, you can comment on the issues in the [issue tracker](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues) or you can [create a new issue](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/new/choose).

To comment on or create discussions and issues, you need to [sign up for a free GitHub account](https://github.com/signup). If you prefer to provide feedback privately, you can email [info@opentelecomdata.net](mailto:info@opentelecomdata.net).
```

OFDS defines schemas based on the [logical data model](../data_model.md) for publishing, storing and exchanging data in the following formats:

```{eval-rst}
.. toctree::
   :maxdepth: 1
   
   json/index.md
   geojson
   csv
   geopackage/index.md
```

Each format provides containers for publishing one or more networks and options to support pagination and streaming, where appropriate.

When sharing data publicly, to support the widest range of use cases, you should publish your data in as many formats as possible so that users can access data in their preferred format.

```{seealso}
For more information on choosing a data format and on publishing data in multiple formats, see [how to format data for publication](../../guidance/publication.md#how-to-format-data-for-publication).
```