# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Superchic(MakefilePackage):
    """SuperChic is a Fortran based Monte Carlo event generator for exclusive and
    photon-initiated production in proton and heavy ion collisions.

    A range of Standard Model final states are implemented, in most cases with
    spin correlations where relevant, and a fully differential treatment of the soft
    survival factor is given. Arbitrary user-defined histograms and cuts may be
    made, as well as unweighted events in the HEPEVT, HEPMC and LHE formats.
    """

    homepage = "https://superchic.hepforge.org/"
    url = "https://superchic.hepforge.org/superchic4.01.tar.gz"

    version("4.01", sha256="2d690e1cdb0fd0ee345028b0d823a76c8d93156aaa0c9cd1ecb5f18cde75acd6")
    version("3.06", sha256="17b4f56e85634f3c9708d5263772d7035fe4d7fb91a11bbffe889e0860efbd02")
    version("3.05", sha256="032f5c784f284ca02003a990234b099f61cd125791d56715680cd342e55c7da1")

    depends_on("fortran", type="build")  # generated

    depends_on("lhapdf")
    depends_on("apfel", when="@4.01:")

    def edit(self, spec, prefix):
        makefile = FileFilter("makefile")
        makefile.filter("LHAPDFLIB = .*", "LHAPDFLIB = " + self.spec["lhapdf"].prefix.lib)
        if self.spec.satisfies("@4.01:"):
            makefile.filter("APFELLIB = .*", "APFELLIB = " + self.spec["apfel"].prefix.lib)

    def build(self, spec, prefix):
        make("PWD=" + self.build_directory)

    def install(self, spec, prefix):
        mkdirp(self.prefix.bin)
        install_tree("bin", self.prefix.bin)

        mkdirp(self.prefix.lib)
        install_tree("lib", self.prefix.lib)

        if self.spec.satisfies("@3.05:"):
            mkdirp(join_path(self.prefix, "src", "inc"))
            install_tree(join_path("src", "inc"), join_path(self.prefix, "src", "inc"))
            mkdirp(join_path(self.prefix, "obj"))
            install_tree("obj", join_path(self.prefix, "obj"))
