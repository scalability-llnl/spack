# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFastdownload(PythonPackage):
    """If you have datasets or other archives that you want to
    make available to your users, and ensure they always have
    the latest versions and that they are downloaded correctly,
    fastdownload can help."""

    homepage = "https://github.com/fastai/fastdownload/tree/master/"
    pypi = "fastdownload/fastdownload-0.0.5.tar.gz"

    license("Apache-2.0")

    version("0.0.5", sha256="64e67af30690fa98ae1c8a1b52495769842f723565239a5430208ad05585af18")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-fastprogress", type=("build", "run"))
    depends_on("py-fastcore@1.3.26:", type=("build", "run"))
