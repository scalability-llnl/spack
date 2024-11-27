# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyXanaduCloudClient(PythonPackage):
    """The Xanadu Cloud Client (XCC) is a Python API and CLI for the Xanadu Cloud."""

    homepage = "https://github.com/XanaduAI/xanadu-cloud-client"
    pypi = "xanadu-cloud-client/xanadu-cloud-client-0.3.0.tar.gz"

    license("Apache-2.0")

    version("0.3.0", sha256="ef65ab7a629e7cd801b20bca8d300d278bf0136c6157c49e12d52c9108171edf")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-appdirs", type=("build", "run"))
    depends_on("py-fire", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pydantic+dotenv", type=("build", "run"))
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
