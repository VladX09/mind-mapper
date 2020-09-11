import os

from setuptools import find_packages, setup


def parse_requirements(requirements_file: str):
    requirements_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), requirements_file)

    with open(requirements_path, "r") as fp:
        return list(fp.readlines())


setup(
    name="mind-mapper",
    version="0.1.1",
    description="Small YAML to Mind Map generator",
    author="Vladislav Verba",
    author_email='vladoladis@gmail.com',
    packages=find_packages(),
    package_data={"mind_mapper": ["themes/*.yml"]},
    install_requires=parse_requirements("requirements.in"),
    entry_points="""
        [console_scripts]
        mind-mapper=mind_mapper.cli:render
    """,
)
