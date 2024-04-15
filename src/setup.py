from setuptools import find_namespace_packages, setup

from autolan.__build__ import version as bld_version

prj_version = bld_version.replace("-", "+", 1).replace("-", ".")  # strict semvers

with open("requirements.in", "r") as f:
    install_requires = f.read().splitlines()

setup(
    name="autolan",
    version=prj_version,
    author="Thiago Lobo",
    author_email="thiagocostalobo@gmail.com",
    description="Python toolset for home LAN automation",
    url="https://github.com/lobothiago/home-lan-automation",
    packages=find_namespace_packages(
        include=["autolan*"], exclude=["*.tests"]
    ),
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "autolan=autolan.cli.main:main"
        ],
    },
)
