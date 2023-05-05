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
#     spack install molgw
#
# You can edit this file again by typing:
#
#     spack edit molgw
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *
from subprocess import run, PIPE


class Molgw(MakefilePackage):
    """MOLGW is a code that implements the many-body perturbation theory (MBPT) to describe the excited electronic states in finite systems (atoms, molecules, clusters).
    MOLGW implements the GW approximation for the self-energy (ionization and affinity) and the Bethe-Salpeter equation for the optical excitations.
    MOLGW also applies the real-time time-dependent density-functional theory (RT-TDDFT).
    MOLGW employs standard Gaussian basis set.
    """

    homepage = "https://github.com/bruneval/molgw"
    url = "https://github.com/bruneval/molgw/archive/v3.1.tar.gz"
    git = "https://github.com/bruneval/molgw.git"

    version("rolling-release", branch="master")
    # version('3.1', sha256='9eb5eadf59d8715c46e9ee8f6eb94e65b7167b9012fc15013803aeafb8ec3a8c')

    depends_on("blas")
    depends_on("lapack")
    depends_on("libxc")
    depends_on("libcint+pypzpx+coulomb_erf")

    variant("openmp", default=False, description="Build with OpenMP support")

    variant("scalapack", default=False, description="Build with ScaLAPACK support")
    depends_on("scalapack", when="+scalapack")
    depends_on("mpi", when="+scalapack")
    depends_on("mpi", when="+scalapack")

    # enforce scalapack capable mkl when asking +scalapack (and using intel-oneapi-mkl)
    depends_on("intel-oneapi-mkl+cluster", when="+scalapack ^intel-oneapi-mkl")
    # enforce threaded openblas when asking +openmp (and using openblas)
    depends_on("openblas threads=openmp", when="+openmp ^openblas")

    # variant('hdf5', default=False, description='Build with HDF5 support')
    # depends_on('hdf5', when='+hdf5')

    def _get_mkl_ld_flags(self,spec):
        #command=["/home/spack/spack-latest/opt/spack/linux-rocky8-skylake_avx512/oneapi-2022.1.0/intel-oneapi-mkl-2023.1.0-22utcrfpxiz3hg36rijq36ln37twer76/mkl/latest/bin/intel64/mkl_link_tool","-libs","--quiet"]
        command=["mkl_link_tool","-libs","--quiet"]
        if "%intel" in spec or "%oneapi" in spec:
            command.extend(["-c","intel_f"])
            if "+openmp" in spec:
                command.extend(["-o","tbb"])
        elif "%gcc" in spec:
            command.extend(["-c","gnu_f"])
            if "+openmp" in spec:
                command.extend(["-o","gomp"])

        if "+scalapack" in spec:
            command.extend(["--cluster_library=scalapack"])
            if "openmpi" in spec:
                command.extend(["-m","openmpi"])
            elif "mpich" in spec:
                command.extend(["-m","mpich2"])
            elif "intelmpi" in spec:
                command.extend(["-m","intelmpi"])
        #result = run(command,capture_output=True, text=True)
        #return result.stdout.strip()
        result = run(command,stdout=PIPE)
        return result.stdout.decode(encoding='utf-8').strip()

    def edit(self, spec, prefix):
        flags = {}
        flags["PREFIX"] = prefix

        # Set LAPACK and SCALAPACK
        if "^mkl" in spec:
            flags["LAPACK"] = self._get_mkl_ld_flags(spec)
        else:
            flags["LAPACK"] = spec["lapack"].libs.ld_flags
            if "+scalapack" in spec:
                flags["SCALAPACK"] = spec["scalapack"].libs.ld_flags
        #print(flags["SCALAPACK"])

        # Set FC
        if "+scalapack" in spec:
            flags["FC"] = "{0}".format(spec["mpi"].mpifc)
        else:
            flags["FC"] = self.compiler.fc_names[0]

        # Set FCFLAGS
        if "%intel" or "%oneapi" in spec in spec:
            flags["FCFLAGS"] = "-fpp "
        else:
            flags["FCFLAGS"] = "-cpp "

        if self.compiler.flags.get("fflags") is not None:
            flags["FCFLAGS"] = ' '.join(self.compiler.flags.get("fflags"))
        if "+openmp" in spec:
            flags["FCFLAGS"] = flags.get("FCFLAGS", "") + " {0}".format(self.compiler.openmp_flag)


        # Set CPPFLAGS
        if "+scalapack" in spec:
            flags["CPPFLAGS"] = flags.get("CPPFLAGS", "") + "-DHAVE_SCALAPACK -DHAVE_MPI "

        if "^mkl" in spec:
            flags["CPPFLAGS"] = flags.get("CPPFLAGS", "") + "-DHAVE_MKL "

        # Write configuration file
        with open("my_machine.arch", "w") as f:
            for k, v in flags.items():
                f.write(k + "=" + v + "\n")

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        make("install")
