# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install pegasus
#
# You can edit this file again by typing:
#
#     spack edit pegasus
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *

class Pegasus(Package):
    """Pegasus is a code which performs a pre-processing step for the Overset CFD
    method. The code prepares the overset volume grids for the flow solver by computing
    the domain connectivity database, and blanking out grid points which are contained
    inside a solid body."""

    homepage = "https://www.nas.nasa.gov/publications/software/docs/pegasus5/pages/sec1.html"
    url = "file:///aerolab/admin/software/dist/pegasus/pegasus5.2d.tar.gz"

    # notify when the package is updated.
    # maintainers("github_user1", "github_user2")

    license("UNKNOWN")

    version("5.2d", sha256="a63a848402d7fa2a2b9960c305c4295fd7a0603288008af43d9cadf5dd68e44b")

    variant("mpi", default=False, description="Enable MPI support")

    depends_on("mpi", when="+mpi")

    phases = ["configure", "build", "install"]

    #./configure $flags --with-installdir=$PEGASUS_DIR/bin_dp --enable-dp --enable-mpi --with-mpif90

    def configure(self, spec, prefix):
        configure(*self.configure_args())


    def configure_args(self):
        spec = self.spec
        prefix = self.prefix

        config_args=[f"--with-installdir={self.prefix}/bin"]

        if "+mpi" in spec:
            config_args.append("--enable-mpi")
            config_args.append("--with-mpif90")

        return config_args


    def build(self, spec, prefix):
        #if "+mpi" in spec:
        #    print(f"spec-mpi = {spec['mpi'].mpicc}")
        #    env["CC"]  = spec["mpi"].mpicc
        #    env["CXX"] = spec["mpi"].mpicxx
        #    env["F77"] = spec["mpi"].mpif77
        #    env["F90"] = spec["mpi"].mpifc

        make("-j1")

    def install(self, spec, prefix):
        make("CMD=install")

    #def setup_run_environment(self, env):
    #    env.prepend_path("PATH", f"{self.prefix}")
