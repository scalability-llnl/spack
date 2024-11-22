# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyArkouda(PythonPackage):
    """This is the python client for Arkouda."""

    homepage = "https://github.com/Bears-R-Us/arkouda"

    # Updating the arkouda PyPI package is future work
    url = "https://github.com/Bears-R-Us/arkouda/archive/refs/tags/v2024.06.21.tar.gz"
    git = "https://github.com/Bears-R-Us/arkouda.git"

    test_requires_compiler = True

    # A list of GitHub accounts to notify when the package is updated.
    # TODO: add arkouda devs github account
    maintainers("arezaii")

    # See https://spdx.org/licenses/ for a list.
    license("MIT")

    version("master", branch="master")

    version(
        "2024.10.02", sha256="00671a89a08be57ff90a94052f69bfc6fe793f7b50cf9195dd7ee794d6d13f23"
    )
    version(
        "2024.06.21", sha256="ab7f753befb3a0b8e27a3d28f3c83332d2c6ae49678877a7456f0fcfe42df51c"
    )

    variant("dev", default=False, description="Include arkouda developer extras")

    depends_on("python@3.8:", type=("build", "run"), when="@:2024.06.21")
    depends_on("python@3.9:3.12.3", type=("build", "run"), when="@2024.10.02:")
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.24.1:1.99", type=("build", "run"))
    depends_on("py-pandas@1.4.0", type=("build", "run"))
    conflicts("^py-pandas@2.2.0", msg="arkouda client not compatible with pandas 2.2.0")

    depends_on("py-pyarrow", type=("build", "run"))
    depends_on("py-pyzmq@20:", type=("build", "run"))
    depends_on("py-scipy@:1.13.1", type=("build", "run"), when="@2024.06.21:")
    depends_on("py-tables@3.7.0: +lzo +bzip2", type=("build", "run"), when="@:2024.06.21")
    depends_on("py-tables@3.8.0: +lzo +bzip2", type=("build", "run"), when="@2024.10.02:")
    depends_on("py-h5py@3.7.0:", type=("build", "run"))
    depends_on("py-matplotlib@3.3.2:", type=("build", "run"))
    depends_on("py-versioneer", type=("build"))
    depends_on("py-pyfiglet", type=("build", "run"))
    depends_on("py-typeguard@2.10:2.12", type=("build", "run"))
    depends_on("py-tabulate", type=("build", "run"))
    depends_on("py-pytest@6.0:", type=("build", "run"), when="@2024.10.02")

    with when("+dev"):
        with default_args(type=("build", "run", "test")):
            # not available in spack: mathjax, sphinx-autoapi, sphinx-autopackagesummary
            # py-myst-parser creates incompatibility with sphinx versions
            depends_on("py-pexpect")
            depends_on("py-pytest@6:")
            depends_on("py-sphinx@5.1.1:")
            depends_on("py-sphinx-argparse")
            depends_on("py-mypy@0.931:")
            depends_on("py-typed-ast")
            depends_on("py-black")
            depends_on("py-isort")
            depends_on("py-flake8")
            depends_on("py-furo")
            # depends_on("py-myst-parser")
            depends_on("py-linkify-it-py")
            depends_on("py-sphinx-design")
            depends_on("py-pandas-stubs")
            depends_on("py-types-python-dateutil")
            depends_on("py-ipython")
