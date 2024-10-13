# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gloo(CMakePackage, CudaPackage):
    """Gloo is a collective communications library."""

    homepage = "https://github.com/facebookincubator/gloo"
    git = "https://github.com/facebookincubator/gloo.git"

    license("BSD-3-Clause")

    version("master", branch="master")
    version("2023-12-03", commit="5354032ea08eadd7fc4456477f7f7c6308818509")  # py-torch@2.3:
    version("2023-05-19", commit="597accfd79f5b0f9d57b228dec088ca996686475")  # py-torch@2.1:2.2
    version("2023-01-17", commit="10909297fedab0a680799211a299203e53515032")  # py-torch@2.0
    version("2022-05-18", commit="5b143513263133af2b95547e97c07cebeb72bf72")  # py-torch@1.13
    version("2021-05-21", commit="c22a5cfba94edf8ea4f53a174d38aa0c629d070f")  # py-torch@1.10:1.12
    version("2021-05-04", commit="6f7095f6e9860ce4fd682a7894042e6eba0996f1")  # py-torch@1.9
    version("2020-09-18", commit="3dc0328fe6a9d47bd47c0c6ca145a0d8a21845c6")  # py-torch@1.7:1.8
    version("2020-03-17", commit="113bde13035594cafdca247be953610b53026553")  # py-torch@1.5:1.6
    version("2019-11-05", commit="7c541247a6fa49e5938e304ab93b6da661823d0f")  # py-torch@1.4
    version("2019-09-29", commit="ca528e32fea9ca8f2b16053cff17160290fc84ce")  # py-torch@1.3
    version("2019-06-19", commit="46ae6ec2191a3cc297ab33d4edd43accc35df992")  # py-torch@1.2
    version("2019-02-01", commit="670b4d4aa46886cc66874e2a4dc846f5cfc2a285")  # py-torch@1.0.1:1.1
    version("2018-11-20", commit="cdeb59d5c82e5401445b4c051bb396f6738d4a19")  # py-torch@1.0.0
    version("2018-05-29", commit="69eef748cc1dfbe0fefed69b34e6545495f67ac5")  # py-torch@0.4.1
    version("2018-04-06", commit="aad0002fb40612e991390d8e807f247ed23f13c5")  # py-torch@:0.4.0

    variant("libuv", default=False, description="Build libuv transport")

    # Gloo does not build on Linux >=6.0.3 (fixed in master)
    # See: https://github.com/facebookincubator/gloo/issues/345
    patch(
        "https://github.com/facebookincubator/gloo/commit/10909297fedab0a680799211a299203e53515032.patch?full_index=1",
        sha256="8e6e9a44e0533ba4303a95a651b1934e5d73632cab08cc7d5a9435e1e64aa424",
        when="@:2023-01-16",
    )
    # Fix building with gcc 12, see https://github.com/facebookincubator/gloo/pull/333
    patch(
        "https://github.com/facebookincubator/gloo/commit/4a5e339b764261d20fc409071dc7a8b8989aa195.patch?full_index=1",
        sha256="dc8b3a9bea4693f32d6850ea2ce6ce75e1778538bfba464b50efca92bac425e3",
        when="@2021-05-21:2022-05-18",
    )

    generator("ninja")
    depends_on("cxx", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("libuv@1.26:", when="+libuv")
    depends_on("cmake@2.8.12:", type="build")
    depends_on("libuv", when="platform=windows")

    def cmake_args(self):
        return [
            self.define_from_variant("USE_CUDA", "cuda"),
            self.define_from_variant("USE_LIBUV", "libuv"),
        ]
