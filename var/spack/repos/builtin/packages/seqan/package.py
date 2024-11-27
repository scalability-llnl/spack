# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Seqan(CMakePackage):
    """SeqAn is an open source C++ library of efficient algorithms and data
    structures for the analysis of sequences with the focus on biological data.
    Our library applies a unique generic design that guarantees high
    performance, generality, extensibility, and integration with other
    libraries. SeqAn is easy to use and simplifies the development of new
    software tools with a minimal loss of performance"""

    homepage = "https://www.seqan.de"
    url = "https://github.com/seqan/seqan/archive/seqan-v2.4.0.tar.gz"

    license("BSD-3-Clause")

    version("2.4.0", sha256="d7084d17729214003e84818e0280a16f223c8f1c6a30eeef040c27e0c0047bd7")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.4.0:", type="build")
    depends_on("python@2.7.0:", type="build")
    depends_on("py-nose", type="build")
    depends_on("py-sphinx", type="build")
    depends_on("boost+exception+math+serialization+container", type=("build", "link"))
    depends_on("zlib-api", type=("build", "link"))
    depends_on("bzip2", type=("build", "link"))

    conflicts("%intel@:16.0.4")
    conflicts("%gcc@:4.9.4")
    conflicts("%llvm@:3.5.1")
