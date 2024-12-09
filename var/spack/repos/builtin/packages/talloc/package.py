# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Talloc(AutotoolsPackage):
    """Talloc provides a hierarchical, reference counted memory pool system
    with destructors. It is the core memory allocator used in Samba."""

    homepage = "https://talloc.samba.org"
    url = "https://www.samba.org/ftp/talloc/talloc-2.1.9.tar.gz"

    license("LGPL-3.0-or-later")

    version("2.4.2", sha256="85ecf9e465e20f98f9950a52e9a411e14320bc555fa257d87697b7e7a9b1d8a6")
    version("2.4.0", sha256="6df36862c42466ef88f360444513870ef46934f9016c84383cc4008a7d0c46ba")
    version("2.3.1", sha256="ef4822d2fdafd2be8e0cabc3ec3c806ae29b8268e932c5e9a4cd5585f37f9f77")
    version("2.3.0", sha256="75d5bcb34482545a82ffb06da8f6c797f963a0da450d0830c669267b14992fc6")
    version("2.1.9", sha256="f0aad4cb88a3322207c82136ddc07bed48a37c2c21f82962d6c5ccb422711062")

    depends_on("c", type="build")  # generated

    extends("python")
    depends_on("python@3:")
