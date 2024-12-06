# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEarthengineApi(PythonPackage):
    """This package allows developers to interact with Google Earth Engine
    using the Python programming language."""

    homepage = "https://github.com/google/earthengine-api"
    pypi = "earthengine-api/earthengine-api-0.1.186.tar.gz"

    license("Apache-2.0")

    version("0.1.344", sha256="bc5a270b8296aaae8574e68dfd93fe878bc5fbe77d1c41f90bcb5e5b830ca5c8")

    depends_on("py-setuptools", type="build")
    depends_on("py-google-cloud-storage", type=("build", "run"))
    depends_on("py-google-api-python-client@1.12.1:", type=("build", "run"))
    depends_on("py-google-api-python-client", type=("build", "run"))
    depends_on("py-google-auth@1.4.1:", type=("build", "run"))
    depends_on("py-google-auth-httplib2@0.0.3:", type=("build", "run"))
    depends_on("py-httplib2@0.9.2:0", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("google-cloud-cli", type="run")
