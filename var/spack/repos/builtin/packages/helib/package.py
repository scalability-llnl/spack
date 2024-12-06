# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Helib(CMakePackage):
    """HElib is an open-source (Apache License v2.0) software library that
    implements homomorphic encryption (HE).

    Currently available schemes are the implementations of the
    Brakerski-Gentry-Vaikuntanathan (BGV) scheme
    with bootstrapping and the Approximate Number scheme of Cheon-Kim-Kim-Song
    (CKKS), along with many optimizations to make homomorphic evaluation run
    faster, focusing mostly on effective use of the Smart-Vercauteren
    ciphertext packing techniques and the Gentry-Halevi-Smart optimizations.
    """

    homepage = "https://github.com/homenc/HElib"
    url = "https://github.com/homenc/HElib/archive/refs/tags/v2.2.1.tar.gz"

    maintainers("wohlbier")

    license("Apache-2.0")

    version("2.2.2", sha256="70c07d2a2da393c695095fe755836524e3d98efb27a336e206291f71db9cec7d")
    version("2.2.1", sha256="cbe030c752c915f1ece09681cadfbe4f140f6752414ab000b4cf076b6c3019e4")
    version("2.2.0", sha256="e5f82fb0520a76eafdf5044a1f17f512999479d899da8c34335da5e193699b94")
    version("2.1.0", sha256="641af0f602cfc7f5f5b1cfde0652252def2dfaf5f7962c2595cf598663637951")
    version("2.0.0", sha256="4e371807fe052ca27dce708ea302495a8dae8d1196e16e86df424fb5b0e40524")
    version("1.3.1", sha256="8ef47092f6b15fbb484a21f9184e7d936c360198515b6efb9a55d3dfbc2ea4be")
    version("1.3.0", sha256="9f69dc5be9197f9ab8cdd81af9a59c12968a0ee11d595b1b1438707ff5405694")
    version("1.2.0", sha256="17e0448a3255ab01a1ebd8382f9d08a318e3d192b56d062a1fd65fbb0aadaf67")
    version(
        "1.1.0-beta.0", sha256="6a454b029f3805101f714f50ae5199e2b2b86c1e520a659f130837810eabe4b5"
    )
    version("1.1.0", sha256="77a912ed3c86f8bde31b7d476321d0c2d810570c04a60fa95c4bd32a1955b5cf")
    version("1.0.2", sha256="b907eaa8381af3d001d7fb8383273f4c652415b3320c11d5be2ad8f19757c998")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("shared", default=False, description="Build shared library.")
    depends_on("gmp@6.2.1:")
    depends_on("ntl@11.5.1:")
    depends_on("ntl+shared", when="+shared")

    def cmake_args(self):
        spec = self.spec
        args = [
            self.define("ENABLE_TEST", "ON"),
            self.define("GMP_DIR", spec["gmp"].prefix),
            self.define("NTL_DIR", spec["ntl"].prefix),
            self.define_from_variant("BUILD_SHARED", "shared"),
        ]

        return args
