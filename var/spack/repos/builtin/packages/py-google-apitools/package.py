# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleApitools(PythonPackage):
    """client libraries for humans"""

    homepage = "https://github.com/google/apitools"
    pypi = "google-apitools/google-apitools-0.5.32.tar.gz"

    maintainers("dorton21")

    license("Apache-2.0")

    version("0.5.32", sha256="c3763e52289f61e21c41d5531e20fbda9cc8484a088b8686fd460770db8bad13")

    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-httplib2@0.8:", type=("build", "run"))
    depends_on("py-fasteners@0.14:", type=("build", "run"))
    depends_on("py-oauth2client@1.4.12:", type=("build", "run"))
    depends_on("py-six@1.12.0:", type=("build", "run"))
