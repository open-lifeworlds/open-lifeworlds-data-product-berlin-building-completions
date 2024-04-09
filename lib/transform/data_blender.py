import json
import os
import re
from functools import reduce

import pandas as pd

from lib.tracking_decorator import TrackingDecorator

key_figure_group = "berlin-lor-building-completions"

prefixes = [
    "including_measures_on_existing_buildings",
    "new_buildings",
    "new_buildings_with_1_and_2_apartments",
    "new_non_residential_buildings"
]

statistic_properties = [
    "buildings",
    "volume",
    "usage_area",
    "apartments",
    "apartments_usage_area",
    "estimated_costs",
]

statistics = [
    f"{key_figure_group}-2020-00",
    f"{key_figure_group}-2021-00",
    f"{key_figure_group}-2022-00"
]


@TrackingDecorator.track_time
def blend_data(source_path, results_path, clean=False, quiet=False):
    # Make results path
    os.makedirs(os.path.join(results_path), exist_ok=True)

    # Initialize statistics
    json_statistics = {}

    # Iterate over LOR area types
    for lor_area_type in ["districts"]:

        # Iterate over statistics
        for statistics_name in sorted(statistics):
            year = re.search(r"\b\d{4}\b", statistics_name).group()
            half_year = re.search(r"\b\d{2}(?<!\d{4})\b", statistics_name).group()

            # Load geojson
            geojson = read_geojson_file(
                os.path.join(source_path, "berlin-lor-geodata", f"berlin-lor-{lor_area_type}.geojson"))

            # Load statistics
            csv_statistics_12 = read_csv_file(os.path.join(source_path, "berlin-building-completions-csv",
                                                           f"berlin-building-completions-{year}-{half_year}-12-completions-by-district-including-measures-on-existing-buildings.csv"))
            csv_statistics_12.rename(
                columns={
                    "district_id": "id",
                    "buildings": "including_measures_on_existing_buildings_buildings",
                    "usage_area": "including_measures_on_existing_buildings_usage_area",
                    "apartments": "including_measures_on_existing_buildings_apartments",
                    "apartments_usage_area": "including_measures_on_existing_buildings_apartments_usage_area",
                    "estimated_costs": "including_measures_on_existing_buildings_estimated_costs"
                }, inplace=True)
            csv_statistics_13 = read_csv_file(os.path.join(source_path, "berlin-building-completions-csv",
                                                           f"berlin-building-completions-{year}-{half_year}-13-completions-by-district-new-buildings.csv"))
            csv_statistics_13.rename(
                columns={
                    "district_id": "id",
                    "buildings": "new_buildings_buildings",
                    "volume": "new_buildings_volume",
                    "usage_area": "new_buildings_usage_area",
                    "apartments": "new_buildings_apartments",
                    "apartments_usage_area": "new_buildings_apartments_usage_area",
                    "estimated_costs": "new_buildings_estimated_costs"
                }, inplace=True)
            csv_statistics_14 = read_csv_file(os.path.join(source_path, "berlin-building-completions-csv",
                                                           f"berlin-building-completions-{year}-{half_year}-14-completions-by-district-new-buildings-with-1-or-2-apartments.csv"))
            csv_statistics_14.rename(
                columns={
                    "district_id": "id",
                    "buildings": "new_buildings_with_1_and_2_apartments_buildings",
                    "volume": "new_buildings_with_1_and_2_apartments_volume",
                    "usage_area": "new_buildings_with_1_and_2_apartments_usage_area",
                    "apartments": "new_buildings_with_1_and_2_apartments_apartments",
                    "apartments_usage_area": "new_buildings_with_1_and_2_apartments_apartments_usage_area",
                    "estimated_costs": "new_buildings_with_1_and_2_apartments_estimated_costs"
                }, inplace=True)
            csv_statistics_15 = read_csv_file(os.path.join(source_path, "berlin-building-completions-csv",
                                                           f"berlin-building-completions-{year}-{half_year}-15-completions-by-district-new-non-residential-buildings.csv"))
            csv_statistics_15.rename(
                columns={
                    "district_id": "id",
                    "buildings": "new_non_residential_buildings_buildings",
                    "volume": "new_non_residential_buildings_volume",
                    "usage_area": "new_non_residential_buildings_usage_area",
                    "apartments": "new_non_residential_buildings_apartments",
                    "apartments_usage_area": "new_non_residential_buildings_apartments_usage_area",
                    "estimated_costs": "new_non_residential_buildings_estimated_costs"
                }, inplace=True)

            # Merge csv statistics
            csv_statistics = reduce(lambda left, right: pd.merge(left, right, on="id", how="outer"),
                                    [csv_statistics_12, csv_statistics_13, csv_statistics_14, csv_statistics_15])

            # Extend geojson
            extend(
                year=year,
                half_year=half_year,
                geojson=geojson,
                statistics_name=statistics_name,
                csv_statistics=csv_statistics,
                json_statistics=json_statistics
            )

            # Write geojson file
            write_geojson_file(
                file_path=os.path.join(results_path, statistics_name,
                                       f"{key_figure_group}-{year}-{half_year}-{lor_area_type}.geojson"),
                statistic_name=f"{key_figure_group}-{year}-{half_year}-{lor_area_type}",
                geojson_content=geojson,
                clean=clean,
                quiet=quiet
            )

    # Write json statistics file
    write_json_file(
        file_path=os.path.join(results_path, f"{key_figure_group}-statistics",
                               f"{key_figure_group}-statistics.json"),
        statistic_name=f"{key_figure_group}-statistics",
        json_content=json_statistics,
        clean=clean,
        quiet=quiet
    )


def extend(year, half_year, geojson, statistics_name, csv_statistics, json_statistics):
    """
    Extends geojson and json-statistics by statistical values
    :param year:
    :param half_year:
    :param geojson:
    :param statistics_name:
    :param csv_statistics:
    :param json_statistics:
    :return:
    """

    # Check for missing files
    if csv_statistics is None:
        print(f"✗️ No data in {statistics_name}")
        return

    # Iterate over features
    for feature in sorted(geojson["features"], key=lambda feature: feature["properties"]["id"]):
        feature_id = feature["properties"]["id"]
        area_sqm = feature["properties"]["area"]
        area_sqkm = area_sqm / 1_000_000

        # Filter statistics
        statistic_filtered = csv_statistics[csv_statistics["id"].astype(str).str.startswith(feature_id)]

        # Check for missing data
        if statistic_filtered.shape[0] == 0:
            print(f"✗️ No data in {statistics_name} for id={feature_id}")
            continue

        # Blend data
        blend_data_into_feature(feature, statistic_filtered, area_sqkm)
        blend_data_into_json(year, half_year, feature_id, feature, json_statistics)

    # Calculate averages
    calculate_averages(year, half_year, geojson, csv_statistics, json_statistics)


def blend_data_into_feature(feature, statistics, area_sqkm):
    # Add new properties
    for prefix, property_name in [(prefix, property_name) for prefix in prefixes for property_name in
                                  statistic_properties]:
        add_property_with_modifiers(feature, statistics, f"{prefix}_{property_name}", area_sqkm)

    return feature


def blend_data_into_json(year, half_year, feature_id, feature, json_statistics):
    # Build structure
    if year not in json_statistics:
        json_statistics[year] = {}
    if half_year not in json_statistics[year]:
        json_statistics[year][half_year] = {}

    # Add properties
    json_statistics[year][half_year][feature_id] = feature["properties"]


def calculate_averages(year, half_year, geojson, csv_statistics, json_statistics):
    # Calculate total values
    total_sqkm = get_total_sqkm(geojson)

    values = {}

    values_sums = {f"{prefix}_{property_name}": int(sum(csv_statistics[f"{prefix}_{property_name}"]))
                   for prefix, property_name in
                   [(prefix, property_name) for prefix in prefixes for property_name in statistic_properties]
                   if f"{prefix}_{property_name}" in csv_statistics}
    values_averages = {}

    if total_sqkm is not None:
        values_averages |= {f"{property_name}_per_sqkm": round(float(total / total_sqkm), 2) for property_name, total in
                            values_sums.items()}

    values |= values_sums
    values |= values_averages

    json_statistics[year][half_year][0] = values


def add_property(feature, statistics, property_name):
    if statistics is not None and property_name in statistics:
        try:
            feature["properties"][f"{property_name}"] = int(statistics[property_name].sum())
        except ValueError:
            feature["properties"][f"{property_name}"] = 0


def add_property_with_modifiers(feature, statistics, property_name, total_area_sqkm):
    if statistics is not None and property_name in statistics:
        try:
            feature["properties"][f"{property_name}"] = int(statistics[property_name].sum())
            if total_area_sqkm is not None:
                feature["properties"][f"{property_name}_per_sqkm"] = round(
                    float(statistics[property_name].sum()) / total_area_sqkm, 2)
        except ValueError:
            feature["properties"][f"{property_name}"] = 0

            if total_area_sqkm is not None:
                feature["properties"][f"{property_name}_per_sqkm"] = 0
        except TypeError:
            feature["properties"][f"{property_name}"] = 0

            if total_area_sqkm is not None:
                feature["properties"][f"{property_name}_per_sqkm"] = 0


def get_total_sqkm(geojson):
    return sum(feature["properties"]["area"] / 1_000_000 for feature in geojson["features"])


def read_csv_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as csv_file:
            return pd.read_csv(csv_file, dtype={"id": "str", "district_id": "str"})
    else:
        return None


def read_geojson_file(file_path):
    with open(file=file_path, mode="r", encoding="utf-8") as geojson_file:
        return json.load(geojson_file, strict=False)


def write_geojson_file(file_path, statistic_name, geojson_content, clean, quiet):
    if not os.path.exists(file_path) or clean:

        # Make results path
        path_name = os.path.dirname(file_path)
        os.makedirs(os.path.join(path_name), exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as geojson_file:
            json.dump(geojson_content, geojson_file, ensure_ascii=False)

            if not quiet:
                print(f"✓ Blend data from {statistic_name} into {os.path.basename(file_path)}")
    else:
        print(f"✓ Already exists {os.path.basename(file_path)}")


def write_json_file(file_path, statistic_name, json_content, clean, quiet):
    if not os.path.exists(file_path) or clean:

        # Make results path
        path_name = os.path.dirname(file_path)
        os.makedirs(os.path.join(path_name), exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(json_content, json_file, ensure_ascii=False)

            if not quiet:
                print(f"✓ Aggregate data from {statistic_name} into {os.path.basename(file_path)}")
    else:
        print(f"✓ Already exists {os.path.basename(file_path)}")
