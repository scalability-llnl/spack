# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPacificaUploader(PythonPackage):
    """Python Pacifica Uploader Library"""

    homepage = "https://github.com/pacifica/pacifica-python-uploader/"
    pypi = "pacifica-uploader/pacifica-uploader-0.3.1.tar.gz"

    license("LGPL-3.0-only")

    version("0.3.1", sha256="adda18b28f01f0b1e6fbaf927fec9b8cf07c86f1b74185bed2a624e8a4597578")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-requests", type=("build", "run"))
