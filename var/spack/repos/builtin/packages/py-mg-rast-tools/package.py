# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMgRastTools(PythonPackage):
    """Repository of scripts and libraries for using the MG-RAST API and
    MG-RAST data."""

    homepage = "https://github.com/MG-RAST/MG-RAST-Tools"
    git = "https://github.com/MG-RAST/MG-RAST-Tools.git"

    version("2018.04.17", commit="a40c6e6539ad0bc1c08e1b03dfc0a9759755a326")

    depends_on("perl", type=("build", "run"))
    depends_on("py-setuptools@28.0:", type="build")
    depends_on("py-prettytable@0.7:", type=("build", "run"))
    depends_on("py-poster@0.8.1:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-requests-toolbelt@0.8:", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("r-matr", type=("build", "run"))
    depends_on("shocklibs@0.1.30:")
    depends_on("perl-list-moreutils", type=("build", "run"))
    depends_on("perl-exporter-tiny", type=("build", "run"))
    depends_on("perl-libwww-perl", type=("build", "run"))
    depends_on("perl-http-message", type=("build", "run"))
    depends_on("perl-json", type=("build", "run"))
