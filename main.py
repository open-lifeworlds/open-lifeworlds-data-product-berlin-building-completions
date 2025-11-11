# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "click>=8.2.1",
#     "open-lifeworlds-python-lib",
# ]
#
# [tool.uv.sources]
# open-lifeworlds-python-lib = { git = "https://github.com/open-lifeworlds/open-lifeworlds-python-lib.git" }
# ///

import os
import sys

import click
from openlifeworlds.config.data_product_manifest_loader import (
    load_data_product_manifest,
)
from openlifeworlds.config.data_transformation_loader import load_data_transformation
from openlifeworlds.config.odps_loader import load_odps
from openlifeworlds.document.data_product_canvas_generator import (
    generate_data_product_canvas,
)
from openlifeworlds.document.data_product_manifest_updater import (
    update_data_product_manifest,
)
from openlifeworlds.document.odps_canvas_generator import generate_odps_canvas
from openlifeworlds.extract.data_extractor import extract_data
from openlifeworlds.metrics.data_metrics_generator import (
    generate_geojson_property_completeness_metrics,
)
from openlifeworlds.transform.data_blender import blend_data

file_path = os.path.realpath(__file__)
script_path = os.path.dirname(file_path)


@click.command()
@click.option("--clean", default=False, help="Regenerate results.")
@click.option("--quiet", default=False, help="Do not log outputs.")
def main(clean, quiet):
    data_path = os.path.join(script_path, "data")
    bronze_path = os.path.join(data_path, "01-bronze")
    silver_path = os.path.join(data_path, "02-silver")
    gold_path = os.path.join(data_path, "03-gold")
    docs_path = os.path.join(script_path, "docs")

    data_product_manifest = load_data_product_manifest(config_path=script_path)
    data_transformation = load_data_transformation(config_path=script_path)
    odps = load_odps(config_path=script_path)

    #
    # Extract
    #

    extract_data(
        data_product_manifest=data_product_manifest,
        results_path=bronze_path,
        clean=clean,
        quiet=quiet,
    )

    #
    # Transform
    #

    blend_data(
        data_product_manifest=data_product_manifest,
        data_transformation=data_transformation,
        source_path=bronze_path,
        results_path=gold_path,
        clean=clean,
        quiet=quiet,
    )

    #
    # Metrics
    #

    generate_geojson_property_completeness_metrics(
        data_product_manifest=data_product_manifest,
        data_transformation=data_transformation,
        config_path=script_path,
        results_path=gold_path,
    )

    #
    # Documentation
    #

    update_data_product_manifest(
        data_product_manifest=data_product_manifest,
        config_path=script_path,
        data_paths=[silver_path, gold_path],
        file_endings=(".geojson", ".json"),
        git_lfs=True,
    )

    generate_data_product_canvas(
        data_product_manifest=data_product_manifest,
        docs_path=docs_path,
    )

    generate_odps_canvas(
        odps=odps,
        docs_path=docs_path,
    )


if __name__ == "__main__":
    main(sys.argv[1:])
