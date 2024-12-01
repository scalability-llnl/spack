# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Vgm(CMakePackage):
    """Virtual Geometry Model (VGM) is a geometry conversion tool, actually
    providing conversion between Geant4 and ROOT TGeo geometry models."""

    homepage = "https://github.com/vmc-project/vgm"
    url = "https://github.com/vmc-project/vgm/archive/v4-8.tar.gz"
    git = "https://github.com/vmc-project/vgm.git"

    tags = ["hep"]

    maintainer = ["wdconinc"]

    license("GPL-3.0-or-later")

    version("master", branch="master")
    version("5-0", sha256="ab929df1aa9b0cda40451f5a98982c3328901865b33e30207ee9b9fe14331344")
    version("4-8", sha256="4fcd607b4f100fc00a65fec7a5803575daf9d4919d1808bbd6a30be263c001dd")
    version("4-7", sha256="a5f5588db457dc3e6562d1f7da1707960304560fbb0a261559fa3f112a476aea")
    version("4-6", sha256="6bf0aeef38f357a313e376090b45d3e0713ef9e52ca198075fae8579b8d5a23a")
    version("4-5", sha256="dc61c6214fdf592dfaa3766eed83cf2bbeabb1755f5146a6d3bcfe55ddbe428f")
    version("4-4", sha256="a915ff3500daa99b74ce9039fbd8abcbd08051e838a1b337e1d794b73537b33b")
    version("4-3", sha256="5cc892a263be2e179a5c2d712c50d7698af7d05d01dfed59c1e36840965f0c4e")
    version("4-2", sha256="25e183f2744fcd4c9995f52865c3f2bf415c7ce0504cfa44093a5f1846a4624f")
    version("4-01", sha256="43020f6497f18086c50e263555c2a21c6cfbba3044b1330c6f400357f040bbb1")
    version("4-00", sha256="c24de76f919dca7c92b3c9fce7a39142c6e61fd39f691d2e4df15fe413b5190d")
    version("3-06", sha256="41948869f2e4dcfa31f4bad42b938c25dd174660c427feb2f9effa9af5e59c7d")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.8:", type="build")
    depends_on("clhep")
    depends_on("root")
    depends_on("geant4")

    def cmake_args(self):
        args = []

        args.append("-DROOT_DIR={0}".format(self.spec["root"].prefix))
        args.append("-DGeant4_DIR={0}".format(self.spec["geant4"].prefix))
        args.append("-DCLHEP_LIB_DIR={0}".format(self.spec["clhep"].prefix.lib))
        args.append("-DCLHEP_INC_DIR={0}".format(self.spec["clhep"].prefix.include))
        args.append("-DWITH_TEST=OFF")

        return args
