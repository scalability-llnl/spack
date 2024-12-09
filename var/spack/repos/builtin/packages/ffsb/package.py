# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ffsb(AutotoolsPackage):
    """The Flexible Filesystem Benchmark (FFSB) is a cross-platform
    filesystem performance measurement tool."""

    homepage = "https://sourceforge.net/projects/ffsb/"
    url = "https://sourceforge.net/projects/ffsb/files/ffsb/5.2.1/ffsb-5.2.1.tar.gz"

    license("GPL-2.0-only")

    version("5.2.1", sha256="36ccda8ff04f837e20bb8b2cc9edb8c6fc923fdcdbb8060d9448dc49234b968d")
    version("5.1.1", sha256="e25aef255d8bfe54f29ac88c7af8237fa5a8c2e1716fdef1946cf0ecd9166d1f")
    version("5.1", sha256="4d7da7eba46c824ebdc23b3d32532b006aeb5b6697a3ada314c75785ab25cb97")

    depends_on("c", type="build")  # generated
