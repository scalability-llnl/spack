# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyObspy(PythonPackage):
    """ObsPy is an open-source project dedicated to provide a Python
    framework for processing seismological data"""

    homepage = "https://github.com/obspy/obspy"
    pypi = "obspy/obspy-1.4.0.tar.gz"

    maintainers("snehring")

    license("LGPL-3.0-only", checked_by="snehring")

    version("1.4.1", sha256="9cf37b0ce03de43d80398703c006bfddbd709f32e8460a9404b27df998d3f747")
    version("1.4.0", sha256="336a6e1d9a485732b08173cb5dc1dd720a8e53f3b54c180a62bb8ceaa5fe5c06")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("python@3.8:3", type=("build", "run"))

    depends_on("py-setuptools", type="build")

    depends_on("py-numpy@1.20:", type=("build", "run"))
    # importing hann from scipy.signal is deprecated, removed in 1.13
    # to be fixed in 1.4.1
    depends_on("py-scipy@1.7:1", type=("build", "run"), when="@1.4.1:")
    depends_on("py-scipy@1.7:1.12.0", type=("build", "run"), when="@1.4.0")
    depends_on("py-matplotlib@3.3:", type=("build", "run"))
    depends_on("py-lxml", type=("build", "run"))
    depends_on("py-sqlalchemy", type=("build", "run"))
    depends_on("py-decorator", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
