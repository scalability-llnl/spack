# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlatbuffers(PythonPackage):
    """
    The FlatBuffers serialization format implemented in Python. For a faster and
    feature-complete version check out the C++ implementation in `flatbuffers`
    package.
    """

    homepage = "https://google.github.io/flatbuffers/"
    pypi = "flatbuffers/flatbuffers-2.0.tar.gz"

    maintainers("gperrotta")

    license("Apache-2.0")

    version("24.3.25", sha256="de2ec5b203f21441716617f38443e0a8ebf3d25bf0d9c0bb0ce68fa00ad546a4")
    version("23.5.26", sha256="9ea1144cac05ce5d86e2859f431c6cd5e66cd9c78c558317c7955fb8d4c78d89")
    version("2.0.7", sha256="0ae7d69c5b82bf41962ca5fde9cc43033bc9501311d975fd5a25e8a7d29c1245")
    version("2.0", sha256="12158ab0272375eab8db2d663ae97370c33f152b27801fa6024e1d6105fd4dd2")
    version("1.12", sha256="63bb9a722d5e373701913e226135b28a6f6ac200d5cc7b4d919fa38d73b44610")

    depends_on("py-setuptools", type="build")
