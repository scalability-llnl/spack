# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIbmWatson(PythonPackage):
    """Python client library to quickly get started with
    the various Watson APIs services."""

    homepage = "https://github.com/watson-developer-cloud/python-sdk"
    pypi = "ibm-watson/ibm-watson-5.1.0.tar.gz"

    license("Apache-2.0")

    version("5.1.0", sha256="faea1e519f6d846a5ca9e03aefc9f894ff8da1eed9117ace6a6fa8f218ba0bc7")

    depends_on("py-setuptools", type="build")
    depends_on("py-requests@2.0:2", type=("build", "run"))
    depends_on("py-python-dateutil@2.5.3:", type=("build", "run"))
    depends_on("py-websocket-client@0.48.0", type=("build", "run"))
    depends_on("py-ibm-cloud-sdk-core@3.3.6:", type=("build", "run"))
