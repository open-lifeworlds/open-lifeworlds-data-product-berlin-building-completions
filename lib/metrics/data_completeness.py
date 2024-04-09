import json
import os
import unittest

file_path = os.path.realpath(__file__)
script_path = os.path.dirname(file_path)

data_path = os.path.join(script_path, "..", "..", "data")

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


class FilesTestCase(unittest.TestCase):
    pass


for year in [2020, 2021, 2022]:
    for half_year in ["00"]:
        for lor_area_type in ["districts"]:
            file = os.path.join(data_path, f"{key_figure_group}-{year}-{half_year}",
                                f"{key_figure_group}-{year}-{half_year}-{lor_area_type}.geojson")
            setattr(
                FilesTestCase,
                f"test_{key_figure_group}_{year}_{half_year}_{lor_area_type}".replace('-', '_'),
                lambda self, file=file: self.assertTrue(os.path.exists(file))
            )


class PropertiesTestCase(unittest.TestCase):
    pass


for year in [2020, 2021, 2022]:
    for half_year in ["00"]:
        for lor_area_type in ["districts"]:
            file = os.path.join(data_path, f"{key_figure_group}-{year}-{half_year}",
                                f"{key_figure_group}-{year}-{half_year}-{lor_area_type}.geojson")
            if os.path.exists(file):
                with open(file=file, mode="r", encoding="utf-8") as geojson_file:
                    geojson = json.load(geojson_file, strict=False)

                for feature in geojson["features"]:
                    feature_id = feature["properties"]["id"]
                    setattr(
                        PropertiesTestCase,
                        f"test_{key_figure_group}_{year}_{half_year}_{lor_area_type}_{feature_id}".replace('-', '_'),
                        lambda self, feature=feature: self.assertTrue(
                            all(f"{prefix}_{property_name}" in feature["properties"] for prefix, property_name in
                                [(prefix, property_name) for prefix in prefixes for property_name in
                                 statistic_properties])
                        )
                    )

if __name__ == '__main__':
    unittest.main()
