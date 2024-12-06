# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Elpa(AutotoolsPackage):
    """Eigenvalue solvers for Petaflop-Applications (ELPA)"""

    homepage = "http://elpa.mpcdf.mpg.de/"
    url = "http://elpa.mpcdf.mpg.de/elpa-2015.11.001.tar.gz"

    version("2018.05.001.rc1", md5="ccd77bd8036988ee624f43c04992bcdd")
    version("2017.11.001", md5="4a437be40cc966efb07aaab84c20cd6e", preferred=True)
    version("2017.05.003", md5="7c8e5e58cafab212badaf4216695700f")
    version("2017.05.002", md5="d0abc1ac1f493f93bf5e30ec8ab155dc")
    version("2016.11.001.pre", md5="5656fd066cf0dcd071dbcaf20a639b37")
    version("2016.05.004", md5="c0dd3a53055536fc3a2a221e78d8b376")
    version("2016.05.003", md5="88a9f3f3bfb63e16509dd1be089dcf2c")
    version("2015.11.001", md5="de0f35b7ee7c971fd0dca35c900b87e6")

    variant("openmp", default=False, description="Activates OpenMP support")
    variant("optflags", default=True, description="Build with optimization flags")

    depends_on("mpi")
    depends_on("blas")
    depends_on("lapack")
    depends_on("scalapack")

    def url_for_version(self, version):
        t = "http://elpa.mpcdf.mpg.de/html/Releases/{0}/elpa-{0}.tar.gz"
        if version < Version("2016.05.003"):
            t = "http://elpa.mpcdf.mpg.de/elpa-{0}.tar.gz"
        return t.format(str(version))

    @property
    def libs(self):
        libname = "libelpa_openmp" if "+openmp" in self.spec else "libelpa"
        return find_libraries(libname, root=self.prefix, shared=True, recursive=True)

    build_directory = "spack-build"

    def setup_run_environment(self, env):
        # TUTORIAL: set the following environment variables:
        #
        # CC=spec['mpi'].mpicc
        # FC=spec['mpi'].mpifc
        # CXX=spec['mpi'].mpicxx
        # SCALAPACK_LDFLAGS=spec['scalapack'].libs.joined()
        #
        # and append the following flags:
        #
        # LDFLAGS -> spec['lapack'].libs.search_flags
        # LIBS -> spec['lapack'].libs.link_flags
        pass

    def configure_args(self):
        # TODO: set optimum flags for platform+compiler combo, see
        # https://github.com/hfp/xconfigure/tree/master/elpa
        # also see:
        # https://src.fedoraproject.org/cgit/rpms/elpa.git/
        # https://packages.qa.debian.org/e/elpa.html
        options = []
        if "+optflags" in self.spec:
            options.extend(["FCFLAGS=-O2 -ffree-line-length-none", "CFLAGS=-O2"])
        if "+openmp" in self.spec:
            options.append("--enable-openmp")
        return options
