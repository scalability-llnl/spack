# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPiper(PythonPackage):
    """A lightweight python toolkit for gluing together restartable,
    robust shell pipelines.
    """

    homepage = "https://github.com/databio/pypiper"
    pypi = "piper/piper-0.12.3.tar.gz"

    license("BSD-2-Clause")

    version("0.12.3", sha256="0ec7d4c4fd9cd1142e87193483c4f92022adbe2cd0f4678f2a1ea8227cdcd9fd")

    depends_on("py-setuptools", type="build")

    depends_on("py-attmap@0.12.5:", type=("build", "run"))
    depends_on("py-logmuse@0.2.4:", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-ubiquerg@0.4.5:", type=("build", "run"))
    depends_on("py-yacman", type=("build", "run"))
