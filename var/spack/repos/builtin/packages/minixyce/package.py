# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Minixyce(MakefilePackage):
    """Proxy Application. A portable proxy of some of the key
    capabilities in the electrical modeling Xyce.
    """

    homepage = "https://mantevo.org"
    url = "https://downloads.mantevo.org/releaseTarballs/miniapps/MiniXyce/miniXyce_1.0.tar.gz"

    tags = ["proxy-app"]

    version("1.0", sha256="40e3b4ed5c65cb1d210e828460e99b755cac922a7e27e70c687d5bb6ed19a21b")

    depends_on("cxx", type="build")  # generated

    variant("mpi", default=True, description="Build with MPI Support")

    depends_on("mpi", when="+mpi")

    @property
    def build_targets(self):
        targets = []

        if "+mpi" in self.spec:
            targets.append("CXX={0}".format(self.spec["mpi"].mpicxx))
            targets.append("LINKER={0}".format(self.spec["mpi"].mpicxx))
            targets.append("USE_MPI=-DHAVE_MPI -DMPICH_IGNORE_CXX_SEEK")
        else:
            targets.append("CXX=c++")
            targets.append("LINKER=c++")
            targets.append("USE_MPI=")

        # Remove Compiler Specific Optimization Flags
        if "%gcc" not in self.spec:
            targets.append("CPP_OPT_FLAGS=")

        return targets

    def build(self, spec, prefix):
        with working_dir("miniXyce_ref"):
            # Call Script Targets First to Generate Needed Files
            make("generate_info")
            make("common_files")
            make(*self.build_targets)

    def install(self, spec, prefix):
        # Manual Installation
        mkdirp(prefix.bin)
        mkdirp(prefix.doc)

        install("miniXyce_ref/miniXyce.x", prefix.bin)
        install("miniXyce_ref/default_params.txt", prefix.bin)
        install("README", prefix.doc)

        install_tree("miniXyce_ref/tests/", prefix.doc.tests)
