# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPystacClient(PythonPackage):
    """Python library for working with Spatiotemporal Asset Catalog (STAC)."""

    homepage = "https://github.com/stac-utils/pystac-client.git"
    pypi = "pystac-client/pystac_client-0.8.5.tar.gz"

    license("Apache-2.0")

    version("0.8.5", sha256="7fba8d4f3c641ff7e840084fc3a53c96443a227f8a5889ae500fc38183ccd994")
    version(
        "0.5.1",
        sha256="f585bd9bcd52ee399c8a292dbb7e0405c0da359a73bc07c1ef82a65c17124d94",
        url="https://files.pythonhosted.org/packages/source/p/pystac-client/pystac-client-0.5.1.tar.gz",
        deprecated=True,
    )

    with default_args(type="build"):
        depends_on("py-setuptools@61:", when="@0.8:")
        depends_on("py-setuptools")

    with default_args(type=("build", "run")):
        depends_on("python@3.10:", when="@0.8:")
        # setup.py imports 'imp', removed in Python 3.12
        depends_on("python@:3.11", when="@:0.6")

        depends_on("py-requests@2.28.2:", when="@0.8:")
        depends_on("py-requests@2.27.1:")
        depends_on("py-pystac@1.10:+validation", when="@0.8:")
        depends_on("py-pystac@1.4:")
        depends_on("py-python-dateutil@2.8.2:", when="@0.8:")
        depends_on("py-python-dateutil@2.7:")
