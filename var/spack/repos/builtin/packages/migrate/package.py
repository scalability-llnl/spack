# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Migrate(AutotoolsPackage):
    """Migrate estimates effective population sizes and past migration rates
    between n population assuming a migration matrix model with asymmetric
    migration rates and different subpopulation sizes"""

    homepage = "https://popgen.sc.fsu.edu/"
    url = "https://popgen.sc.fsu.edu/currentversions/migrate-3.6.11.src.tar.gz"

    license("Unlicense")

    version("3.6.11", sha256="a9ba06a4e995a45b8d04037f5f2da23e1fe64a2f3565189bdd50c62c6fe01fb8")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("mpi", default=False, description="Build MPI binaries")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("zlib-api", type="link")

    depends_on("openmpi", type=("build", "link", "run"), when="+mpi")

    configure_directory = "src"

    def configure_args(self):
        return ["--with-zlib=system"]

    def build(self, spec, prefix):
        with working_dir("src"):
            # this software is written with parts both in C and C++.
            # it tries to link using gcc which causes problems, so this package
            # explicitly links with g++ (CXX) instead.

            # spack's FileFilter/filter_file only work per-line (see docs),
            # so the package uses a custom filter by replacing substrings
            # in the Makefile.

            mfc = ""
            with open("Makefile") as m:
                mfc = mfc_old = m.read()

                # replace linking step
                mfc = mfc.replace(
                    "$(NAME): $(PRODUCT_DEPENDS)\n\t$(CC)", "$(NAME): $(PRODUCT_DEPENDS)\n\t$(CXX)"
                )
                mfc = mfc.replace(
                    "$(MPINAME): $(PRODUCT_DEPENDS)\n\t$(CC)",
                    "$(MPINAME): $(PRODUCT_DEPENDS)\n\t$(CXX)",
                )

                # make sure the replace worked
                if mfc == mfc_old:
                    raise InstallError("Failed to update linker command")

                # don't try to install MPI binaries that aren't there
                if "+mpi" not in spec:
                    line = "$(INSTALL) $(IFLAGS) $(MPINAME) $(INSTALLDIR)"
                    mfc = mfc.replace(line, "")

            # write modified makefile back
            with open("Makefile", "w") as m:
                m.write(mfc)

            make()
            if "+mpi" in spec:
                make("mpis")

    def install(self, spec, prefix):
        mkdirp(prefix.man)
        with working_dir("src"):
            make("install")
