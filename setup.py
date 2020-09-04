from setuptools import setup, find_packages
# TODO: add more info

setup(
    name="mind-mapper",
    version="0.1",
    packages=find_packages(),
    package_data={"mind_mapper": ["themes/*.yml"]},
    # install_requires=[],
    entry_points="""
        [console_scripts]
        mind-mapper=cli:render
    """,
)
