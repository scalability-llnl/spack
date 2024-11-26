# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyJanus(PythonPackage):
    """Thread-safe asyncio-aware queue for Python"""

    homepage = "https://github.com/aio-libs/janus"
    pypi = "janus/janus-1.0.0.tar.gz"

    maintainers("teaguesterling")

    license("APACHE-2.0", checked_by="teaguesterling")

    version("1.0.0", sha256="df976f2cdcfb034b147a2d51edfc34ff6bfb12d4e2643d3ad0e10de058cb1612")
    version("0.7.0", sha256="f10dcf5776e8d49cc30ec86d5eb7268eeec39abaa24fe0332ee8fb8fa3611845")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools@51:", type="build")
    depends_on("py-wheel@0.36:", type="build")
