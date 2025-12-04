
# Data Product Canvas - Berlin Building Completions

## Metadata

* owner: Open Lifeworlds
* description: Data product Berlin building completion data on different hierarchy levels
* updated: 2025-11-09

## Input Ports

### berlin-lor-geodata

* manifest URL: https://raw.githubusercontent.com/open-data-product/open-data-product-berlin-lor-geodata/refs/heads/main/data-product-manifest.yml

### berlin-lor-building-completions-source-aligned

* manifest URL: https://raw.githubusercontent.com/open-data-product/open-data-product-berlin-building-completions-source-aligned/refs/heads/main/data-product-manifest.yml

## Transformation Steps

* [Data extractor](https://github.com/open-lifeworlds/open-lifeworlds-python-lib/blob/main/openlifeworlds/extract/data_extractor.py) extracts data from inout ports
* [Data blender](https://github.com/open-lifeworlds/open-lifeworlds-python-lib/blob/main/openlifeworlds/transform/data_blender.py) blends csv data into geojson files

## Output Ports

### berlin-building-completions-geojson
name: Berlin Building Completions Geojson
* owner: Open Lifeworlds
* url: https://github.com/open-lifeworlds/open-lifeworlds-data-product-berlin-building-completions/tree/main/data/03-gold/berlin-building-completions-geojson
* updated: 2025-11-09

**Files**

* [berlin-building-completions-2020-00-districts.geojson](https://media.githubusercontent.com/media/open-lifeworlds/open-lifeworlds-data-product-berlin-building-completions/refs/heads/main/data/03-gold/berlin-building-completions-geojson/berlin-building-completions-2020-00-districts.geojson)
* [berlin-building-completions-2021-00-districts.geojson](https://media.githubusercontent.com/media/open-lifeworlds/open-lifeworlds-data-product-berlin-building-completions/refs/heads/main/data/03-gold/berlin-building-completions-geojson/berlin-building-completions-2021-00-districts.geojson)
* [berlin-building-completions-2022-00-districts.geojson](https://media.githubusercontent.com/media/open-lifeworlds/open-lifeworlds-data-product-berlin-building-completions/refs/heads/main/data/03-gold/berlin-building-completions-geojson/berlin-building-completions-2022-00-districts.geojson)
* [berlin-building-completions-2023-00-districts.geojson](https://media.githubusercontent.com/media/open-lifeworlds/open-lifeworlds-data-product-berlin-building-completions/refs/heads/main/data/03-gold/berlin-building-completions-geojson/berlin-building-completions-2023-00-districts.geojson)


### berlin-building-completions-statistics
name: Berlin Building Completions Statistics
* owner: Open Lifeworlds
* url: https://github.com/open-lifeworlds/open-lifeworlds-data-product-berlin-building-completions/tree/main/data/03-gold/berlin-building-completions-statistics
* updated: 2025-11-09

**Files**

* [berlin-building-completions-statistics.json](https://media.githubusercontent.com/media/open-lifeworlds/open-lifeworlds-data-product-berlin-building-completions/refs/heads/main/data/03-gold/berlin-building-completions-statistics/berlin-building-completions-statistics.json)


## Observability

### Quality metrics

 * name: geojson_property_completeness
 * description: The percentage of geojson features that have all necessary properties

| Name | Value |
| --- | --- |
| berlin-building-completions-2020-00-districts.geojson | 44 |
| berlin-building-completions-2021-00-districts.geojson | 43 |
| berlin-building-completions-2022-00-districts.geojson | 42 |
| berlin-building-completions-2023-00-districts.geojson | 42 |


## Classification

**The nature of the exposed data (source-aligned, aggregate, consumer-aligned)**

consumer-aligned


---
This data product canvas uses the template of [datamesh-architecture.com](https://www.datamesh-architecture.com/data-product-canvas).