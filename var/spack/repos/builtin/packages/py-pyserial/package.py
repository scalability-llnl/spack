# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyserial(PythonPackage):
    """Python Serial Port Extension"""

    homepage = "https://github.com/pyserial/pyserial"
    pypi = "pyserial/pyserial-3.1.1.tar.gz"

    license("BSD-3-Clause")

    version("3.1.1", sha256="d657051249ce3cbd0446bcfb2be07a435e1029da4d63f53ed9b4cdde7373364c")

    depends_on("py-setuptools", type="build")
