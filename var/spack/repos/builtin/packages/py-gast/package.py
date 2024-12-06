# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGast(PythonPackage):
    """Python AST that abstracts the underlying Python version"""

    homepage = "https://github.com/serge-sans-paille/gast"
    pypi = "gast/gast-0.3.2.tar.gz"

    license("BSD-3-Clause")

    version("0.5.4", sha256="9c270fe5f4b130969b54174de7db4e764b09b4f7f67ccfc32480e29f78348d97")
    version("0.5.3", sha256="cfbea25820e653af9c7d1807f659ce0a0a9c64f2439421a7bba4f0983f532dea")
    version("0.5.2", sha256="f81fcefa8b982624a31c9e4ec7761325a88a0eba60d36d1da90e47f8fe3c67f7")
    version("0.5.1", sha256="b00e63584db482ffe6107b5832042bbe5c5bf856e3c7279b6e93201b3dcfcb46")
    version("0.5.0", sha256="8109cbe7aa0f7bf7e4348379da05b8137ea1f059f073332c3c1cedd57db8541f")
    version("0.4.0", sha256="40feb7b8b8434785585ab224d1568b857edb18297e5a3047f1ba012bc83b42c1")
    version("0.3.3", sha256="b881ef288a49aa81440d2c5eb8aeefd4c2bb8993d5f50edae7413a85bfdb3b57")
    version("0.3.2", sha256="5c7617f1f6c8b8b426819642b16b9016727ddaecd16af9a07753e537eba8a3a5")
    version("0.2.2", sha256="fe939df4583692f0512161ec1c880e0a10e71e6a232da045ab8edd3756fbadf0")
    version("0.2.0", sha256="7068908321ecd2774f145193c4b34a11305bd104b4551b09273dfd1d6a374930")

    depends_on("py-setuptools", type="build")
