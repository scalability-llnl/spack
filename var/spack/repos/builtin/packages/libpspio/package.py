# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libpspio(AutotoolsPackage):
    """Library to perform I/O operations on pseudopotential data files."""

    homepage = "https://gitlab.com/ElectronicStructureLibrary/libpspio"
    url = "https://gitlab.com/ElectronicStructureLibrary/libpspio/-/archive/0.3.0/libpspio-0.3.0.tar.gz"

    maintainers("hmenke")

    license("MPL-2.0")

    version("0.4.1", sha256="e4f87f6d8821042db3a88dad60ae07278e36ad2571e28f5d30f02d8b164b4daa")
    version("0.3.0", sha256="4dc092457e481e5cd703eeecd87e6f17749941fe274043550c8a2557a649afc5")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("fortran", default=False, description="Enable Fortran bindings")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("check")
    depends_on("gsl")

    def autoreconf(self, spec, prefix):
        Executable("./autogen.sh")()

    def configure_args(self):
        args = self.enable_or_disable("fortran")
        return args
