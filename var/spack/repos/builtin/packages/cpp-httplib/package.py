# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CppHttplib(CMakePackage):
    """A C++ header-only HTTP/HTTPS server and client library."""

    homepage = "https://github.com/yhirose/cpp-httplib/"
    url = "https://github.com/yhirose/cpp-httplib/archive/v0.5.10.tar.gz"

    license("MIT")

    version("0.15.3", sha256="2121bbf38871bb2aafb5f7f2b9b94705366170909f434428352187cb0216124e")
    version("0.12.5", sha256="b488f3fa9c6bf35608c3d9a5b69be52e016bbf2fbfe67e5ee684eadb2655493e")
    version("0.12.3", sha256="175ced3c9cdaf221e9edf210297568d8f7d402a41d6db01254ac9e0b25487c54")
    version("0.5.9", sha256="c9e7aef3b0d4e80ee533d10413508d8a6e09a67d0d59646c43111f3993de006e")
    version("0.5.8", sha256="184d4fe79fc836ee26aa8635b3240879af4c6f17257fc7063d0b77a0cf856dfc")
    version("0.5.7", sha256="27b7f6346bdeb1ead9d17bd7cea89d9ad491f50f0479081053cc6e5742a89e64")
    version("0.5.6", sha256="06ebc94edcdf23d66692bf1d128f6c65bb0ec36ce5e2f8ee61990bc74e838868")
    version("0.5.5", sha256="e18dab82b3b395290514baf3804c7b74892beb654bd8020600a9d9dfdc49c32a")
    version("0.5.4", sha256="40dcce66ec002e2631ef918e1b3bfc9ec1662d02007291ea4743e17ac9c7d43f")
    version("0.5.3", sha256="d9d62ae15d5a2f4404286d5f6ec48daef27e24b5aab98d0505e24ee2b187d3f5")
    version("0.5.2", sha256="a28cc74d3b46e2ba60311b9229375599b513151e39a7d8df6fe1fb797fc1be3a")
    version("0.5.1", sha256="e079d1803e4fdbaf8bed5b414f6045c78273082eec7ac0d4802029175f2a1448")
    version("0.4.2", sha256="ceaf50e2a9fce48910b244d33c6824e55aef688ad5bc181f4b9504242c2447ff")
    version("0.3.3", sha256="476471c6fcd4b39fc79a5dd6ad343a2428cb69b4d528557abb6a0b7bf8186e34")
    version("0.2.6", sha256="8678afc0e69bc198edcb8fe0066e46a87373221232ebabde2d78c237f31d3c3d")
    version("0.2.1", sha256="94a6ddd25088b66b7b9e57b9d0ea138c984967e91b21395401642027bf279438")

    depends_on("cxx", type="build")  # generated
