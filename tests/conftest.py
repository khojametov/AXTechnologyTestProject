import os

os.environ["SETTINGS_MODULE"] = "config.settings.test"

fixture_plugins = ["tests.fixtures.database"]

pytest_plugins = [
    "tests.factory_register",
    "tests.fixtures.database",
    "tests.fixtures.api",
    "tests.fixtures.general",
]
