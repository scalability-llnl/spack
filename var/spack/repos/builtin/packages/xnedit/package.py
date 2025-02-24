# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xnedit(MakefilePackage):
    """XNEdit is a multi-purpose text editor for the X Window System, which combines a standard,
    easy to use, graphical user interface with the thorough functionality and stability."""

    license("GPL-2.0-or-later")

    homepage = "https://www.unixwork.de/xnedit/"
    url = "https://github.com/unixwork/xnedit/archive/refs/tags/v1.6.1.tar.gz"
    git = "https://github.com/unixwork/xnedit.git"

    maintainers("davekeeshan")

    version("1.6.2", sha256="0ee832ad186b81b8ba8df43352d86e35997cea9708ff7ddad15e9d91fe81b6cb")
    version("1.6.1", sha256="46489fa3017f5e40da810170b33c681affd3cd4dff1dbd0f8a4c51f8285ca5c4")
    version("1.6.0", sha256="197e635fc1aa8e4ff2dcd2375efac597975f04170c3eace3280c4054bbbc57ac")
    version("1.5.3", sha256="89421abbcb91f27e122b874769ca60021802735ea527fc6ae5b3d50061f81120")
    version("1.5.2", sha256="2f9710b661f8ec5d371a3385fa480c7424e2f863938a8e2ae71cb17397be3f91")
    version("1.5.1", sha256="c871589e912ed9f9a02cc57932f5bb9694ec91cc5487be0cd55e7d3aade372d6")
    version("1.5.0", sha256="054f0805405bfc0304e5d27aaac7f4d89b9f028b9e408bf8c079669ddb89df00")
    version("1.4.1", sha256="6f6ef827b0f6efe481333fe81ec30e2ab133b24cbc9bab224c02e1f69474bade")
    version("1.4.0", sha256="91c88689c853a6f16f22c109a7283ae552a7079829a25dfa6db192b3d6c6cb60")
    version("1.3.3", sha256="388765726bca2887eca4a95e1253214ee7209075b0bdd4a143ad870ccc04703f")
    version("1.3.2", sha256="20f816dba7c3aa59504d1a1360a731854581801c3031012a6b8fef55d437bd04")
    version("1.3.1", sha256="e1551983cb4e6ee8c9dcb35a628fdcf12dd191bab9321c98c77c22456688e81a")
    version("1.3.0", sha256="5b1fccbaee007dceca37b24d248e27818c30eb0a87b79317f51ba731da3b8a03")
    version("1.2.2", sha256="9d0434fb47a306f8665bcf4f9bf3f41173c31010cdfd767a0622ae8b9be10ac1")
    version("1.2.1", sha256="e0c0147c7f81ccac1c40acb5636b375ef76678a7a84ec592d509461af00983c5")
    version("1.2.0", sha256="8a6a1252b36be8be5c20aafe5989ad3158cd66449632bf1014ad10cf85a6ea16")
    version("1.1.1", sha256="9958cc58f9834e3ccfa1d094e942f1ff5bc8b0464ae8e6d259cbb9e71bfb1ebd")
    version("1.1.0", sha256="c335c3a5beb2263d5a9974931dbdd1f2e5cf77fd0eafd4026ee2b7ca0aad2fe7")
    version("1.0.1", sha256="3efa26d180696ea7b24c3efd2599c52183b6851fc1bc87ce9a4f85d465962a8c")
    version("1.0.0", sha256="f58dcbd268f226192584f56dd1a897290a66176d91a90d715a40d63578a84b72")

    depends_on("automake", type="build")
    depends_on("libx11")
    depends_on("libxt")
    depends_on("libxpm")
    depends_on("motif")
    depends_on("pcre")

    def setup_build_environment(self, env):
        env.prepend_path("LDFLAGS", "-Wl,--copy-dt-needed-entries")

    def build(self, spec, prefix):
        make("linux")

    def install(self, spec, prefix):
        make("install", f"PREFIX={prefix}")
