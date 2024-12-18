# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBitarray(PythonPackage):
    """Efficient array of booleans - C extension"""

    pypi = "bitarray/bitarray-0.8.1.tar.gz"

    version("2.7.6", sha256="3807f9323c308bc3f9b58cbe5d04dc28f34ac32d852999334da96b42f64b5356")
    version("2.7.4", sha256="143d4f65e1f45a533e13521be1dc557a782317ecf76520eabd5a903b26ecb187")
    version("2.6.0", sha256="56d3f16dd807b1c56732a244ce071c135ee973d3edc9929418c1b24c5439a0fd")
    version("0.8.1", sha256="7da501356e48a83c61f479393681c1bc4b94e5a34ace7e08cb29e7dd9290ab18")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
