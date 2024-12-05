# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySseclient(PythonPackage):
    """This is a Python client library for iterating over http Server
    Sent Event (SSE) streams
    """

    homepage = "https://github.com/btubbs/sseclient"
    pypi = "sseclient/sseclient-0.0.27.tar.gz"

    license("MIT")

    version("0.0.27", sha256="b2fe534dcb33b1d3faad13d60c5a7c718e28f85987f2a034ecf5ec279918c11c")

    depends_on("py-setuptools", type="build")
    depends_on("py-requests@2.9:", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
