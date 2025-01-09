# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsdf(PythonPackage):
    """The Advanced Scientific Data Format (ASDF) is a next-generation
    interchange format for scientific data. This package contains the Python
    implementation of the ASDF Standard."""

    homepage = "https://asdf.readthedocs.io/"
    pypi = "asdf/asdf-2.15.0.tar.gz"

    maintainers("lgarrison")

    license("BSD-3-Clause")

    version("3.5.0", sha256="047ad7bdd8f40b04b8625abfd119a35d18b344301c60ea9ddf63964e7ce19669")
    version("2.15.0", sha256="686f1c91ebf987d41f915cfb6aa70940d7ad17f87ede0be70463147ad2314587")
    version("2.4.2", sha256="6ff3557190c6a33781dae3fd635a8edf0fa0c24c6aca27d8679af36408ea8ff2")

    variant("lz4", default=True, description="Enable lz4 compression")

    depends_on("py-lz4@0.10:", when="+lz4", type=("build", "run"))

    with when("@3.5.0:"):
        depends_on("python@3.9:", type=("build", "run"))

        depends_on("py-asdf-standard@1.1.0:", type=("build", "run"))
        depends_on("py-importlib-metadata@4.11.4:", type=("build", "run"), when="^python@:3.11")
        depends_on("py-numpy@1.22:", type=("build", "run"))
        depends_on("py-attrs@22.2.0:", type=("build", "run"))

    with when("@2.15.0:"):
        depends_on("python@3.8:", type=("build", "run"))

        depends_on("py-setuptools@60:", type="build")
        depends_on("py-setuptools-scm@3.4: +toml", type="build")

        depends_on("py-asdf-standard@1.0.1:", type=("build", "run"))
        depends_on("py-asdf-transform-schemas@0.3:", type=("build", "run"))
        depends_on("py-jmespath@0.6.2:", type=("build", "run"))
        depends_on("py-numpy@1.20:", type=("build", "run"))
        depends_on("py-packaging@19:", type=("build", "run"))
        depends_on("py-pyyaml@5.4.1:", type=("build", "run"))
        depends_on("py-semantic-version@2.8:", type=("build", "run"))

    with when("@2.15.0"):
        depends_on("py-asdf-unit-schemas@0.1:", type=("build", "run"))
        depends_on("py-importlib-metadata@4.11.4:", type=("build", "run"))
        depends_on("py-importlib-resources@3:", type=("build", "run"), when="^python@:3.8")
        depends_on("py-jsonschema@4.0.1:4.17", type=("build", "run"))
        depends_on("py-numpy@1.20:1.24", type=("build", "run"), when="^python@:3.8")

    with when("@2.4.2"):
        depends_on("python@3.3:", type=("build", "run"))

        depends_on("py-setuptools@30.3.0:", type="build")
        depends_on("py-setuptools-scm", type="build")

        depends_on("py-semantic-version@2.3.1:2.6.0", type=("build", "run"))
        depends_on("py-pyyaml@3.10:", type=("build", "run"))
        depends_on("py-jsonschema@2.3:3", type=("build", "run"))
        depends_on("py-six@1.9.0:", type=("build", "run"))
        depends_on("py-numpy@1.8:", type=("build", "run"))
