# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibmmtfCpp(CMakePackage):
    """The macromolecular transmission format (MMTF) is a binary encoding of
    biological structures. This repository holds the C++-03 compatible API,
    encoding and decoding libraries."""

    homepage = "https://github.com/rcsb/mmtf-cpp"
    url = "https://github.com/rcsb/mmtf-cpp/archive/v1.0.0.tar.gz"

    version("1.1.0", sha256="021173bdc1814b1d0541c4426277d39df2b629af53151999b137e015418f76c0")
    version("1.0.0", sha256="881f69c4bb56605fa63fd5ca50842facc4947f686cbf678ad04930674d714f40")

    depends_on("cxx", type="build")  # generated

    depends_on("msgpack-c")
