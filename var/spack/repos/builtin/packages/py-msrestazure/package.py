# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMsrestazure(PythonPackage):
    """AutoRest swagger generator Python client runtime.
    Azure-specific module."""

    homepage = "https://github.com/Azure/msrestazure-for-python"
    pypi = "msrestazure/msrestazure-0.6.3.tar.gz"

    version("0.6.3", sha256="0ec9db93eeea6a6cf1240624a04f49cd8bbb26b98d84a63a8220cfda858c2a96")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.6.0:1", type=("build", "run"))
    depends_on("py-adal@0.6.0:1", type=("build", "run"))
