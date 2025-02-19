# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *


class Paraconf(CMakePackage):
    """Paraconf is a library that provides a simple query language to access a
    Yaml tree on top of libyaml."""

    homepage = "https://github.com/pdidev/paraconf"
    url = "https://github.com/pdidev/paraconf/archive/1.0.0.tar.gz"

    license("BSD-3-Clause")

    maintainers("jbigot")

    version("1.0.0", sha256="9336492c292088a7d97192f2b1fa306e11f6f32373ac75f29b9af7eecd5c0c11")
    version("0.4.16", sha256="d896cb5bbf1c6b311f6bed44263548c799265e1f22d50475aecbddc80b0db982")
    version("0.4.15", sha256="914befa7a8d6fbf2de3466e434a9ea20363900af5519859663a24c7a51bd26a6")
    version("0.4.14", sha256="8a07bdf972ce137932b0d5e08036cf90db23b69f7eaabf52eb7d495d1da01d99")
    version("0.4.13", sha256="28da96ba45bcb826a387488f283baa0c88bc0b00fa74f4c110d444c0b9a8030c")
    version("0.4.12", sha256="bbbaf462ed23e9a64a4d521ee469ab723fcd86a6dda9a9d9b4dddfd1a58eef93")
    version("0.4.11", sha256="35f4ba41eaf675ff16ad4f0722a9e2050ee63b073c7e3e67eb74439978599499")
    version("0.4.10", sha256="0a0028354b131436e70af06c9e029f738ed771088e53633b2b5d1c8ee1276e83")
    version("0.4.9", sha256="e99a01584e07e4d09b026fcd9a39500fbdbc3074a2598a4bc89f400825094c5a")

    variant("shared", default=True, description="Build shared libraries rather than static ones")
    variant("fortran", default=True, description="Enable Fortran support")
    variant("tests", default=False, description="Build tests")

    depends_on("cmake@3.5:", type=("build"))
    depends_on("pkgconfig", type=("build"))
    depends_on("libyaml@0.1.7:", type=("link", "run"))

    root_cmakelists_dir = "paraconf"

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("BUILD_TESTING", "tests"),
            self.define_from_variant("BUILD_FORTRAN", "fortran"),
        ]
        return args
