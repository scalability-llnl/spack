# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibatomicOps(AutotoolsPackage):
    """This package provides semi-portable access to hardware-provided
    atomic memory update operations on a number architectures."""

    homepage = "https://www.hboehm.info/gc/"
    url = "https://github.com/ivmai/libatomic_ops/releases/download/v7.8.0/libatomic_ops-7.8.0.tar.gz"

    license("GPL-2.0-only")

    version("7.8.2", sha256="d305207fe207f2b3fb5cb4c019da12b44ce3fcbc593dfd5080d867b1a2419b51")
    version("7.8.0", sha256="15676e7674e11bda5a7e50a73f4d9e7d60452271b8acf6fd39a71fefdf89fa31")
    version("7.6.14", sha256="390f244d424714735b7050d056567615b3b8f29008a663c262fb548f1802d292")
    version("7.6.12", sha256="f0ab566e25fce08b560e1feab6a3db01db4a38e5bc687804334ef3920c549f3e")
    version("7.6.6", sha256="99feabc5f54877f314db4fadeb109f0b3e1d1a54afb6b4b3dfba1e707e38e074")
    version("7.4.4", sha256="bf210a600dd1becbf7936dd2914cf5f5d3356046904848dcfd27d0c8b12b6f8f")

    depends_on("c", type="build")  # generated

    def configure_args(self):
        return ["--enable-shared"]
