# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cudd(AutotoolsPackage):
    """
    The CUDD package is a package written in C for the manipulation of
    decision diagrams.  It supports binary decision diagrams (BDDs),
    algebraic decision diagrams (ADDs), and Zero-Suppressed BDDs (ZDDs).
    """

    homepage = "https://cudd-mirror.sourceforge.io"
    url = "https://sourceforge.net/projects/cudd-mirror/files/cudd-3.0.0.tar.gz"

    maintainers("davekeeshan")

    version("3.0.0", sha256="b8e966b4562c96a03e7fbea239729587d7b395d53cadcc39a7203b49cf7eeb69")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
