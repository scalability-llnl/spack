# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nvdimmsim(MakefilePackage):
    """
    NVDIMMSim is a cycle-accurate non-volatile memory simulator
    for devices such as NAND flash
    """

    homepage = "https://github.com/slunk/NVDIMMSim"
    git = "https://github.com/slunk/NVDIMMSim"
    url = "https://github.com/jimstevens2001/NVDIMMSim/archive/v2.0.0.tar.gz"

    maintainers("jjwilke")

    version("2.0.0", sha256="2a621ef10be5e52a1f543985d08354a2e6ee6532b5720e5f17ad6362cfd4adef")

    depends_on("cxx", type="build")  # generated

    def build(self, spec, prefix):
        with working_dir("src"):
            if spec.satisfies("platform=darwin"):
                make("libnvdsim.dylib")
            else:
                make("libnvdsim.so")

    def install(self, spec, prefix):
        with working_dir("src"):
            install_tree(".", prefix)
