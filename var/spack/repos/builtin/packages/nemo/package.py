# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nemo(Package):
    """The "Nucleus for European Modelling of the Ocean" (NEMO) is a
    state-of-the-art modelling framework. It is used for research
    activities and forecasting services in ocean and climate sciences.
    NEMO is developed by a European consortium with the
    objective of ensuring long term reliability and sustainability."""

    homepage = "https://www.nemo-ocean.eu/"
    git = "https://forge.nemo-ocean.eu/nemo/nemo.git"

    version("4.2.1", tag="v4.2.1", commit="9c0f2d511690c30aec45516361e032c5b46a94f5")
    version("4.2.0", tag="v4.2.0", commit="5cf0c3d61b751a102fe9de9c8ffe61a7216946cc")

    depends_on("mpi")
    depends_on("xios@develop-2612")
    depends_on("perl")
    depends_on("netcdf-c+mpi")
    depends_on("netcdf-fortran")
    depends_on("hdf5+mpi")

    # Avoided build errors that occur when reading internal files containing
    # multiple namelists for Fujitsu compilers
    patch(
        "https://github.com/fujitsu/oss-patches-for-a64fx/blob/master/Nemo/fj-v4.2.0.patch",
        when="@4.2.0%fj",
    )
    patch(
        "https://github.com/fujitsu/oss-patches-for-a64fx/blob/master/Nemo/fj-v4.2.1.patch",
        when="@4.2.1%fj",
    )

    def nemo_fcm(self):
        file = join_path("arch", "arch-SPACK.fcm")
        spec = self.spec
        param = dict()
        param["MPIFC"] = spec["mpi"].mpifc
        param["CC"] = self.compiler.cc
        param["HDF5_INC"] = spec["hdf5"].prefix.include
        param["HDF5_LIB"] = spec["hdf5"].prefix.lib
        param["NCDF_C_INC"] = spec["netcdf-c"].prefix.include
        param["NCDF_C_LIB"] = spec["netcdf-c"].prefix.lib
        param["NCDF_F_INC"] = spec["netcdf-fortran"].prefix.include
        param["NCDF_F_LIB"] = spec["netcdf-fortran"].prefix.lib
        param["XIOS_INC"] = spec["xios"].prefix.include
        param["XIOS_LIB"] = spec["xios"].prefix.lib
        if spec.satisfies("%fj"):
            param["LD"] = spec["mpi"].mpifc
            param["LIBCXX"] = "-std=c++03 --linkfortran"
            param["FFLAGS"] = "-CcdRR8 -O3"
        else:
            param["LD"] = spec["mpi"].mpicxx
            param["LIBCXX"] = ""
            param["FFLAGS"] = (
                "-fdefault-real-8 -O3 -funroll-all-loops -fcray-pointer -ffree-line-length-none"
            )
        text = r"""
%NCDF_INC            -I{NCDF_F_INC} -I{NCDF_C_INC} -I{HDF5_INC}
%NCDF_LIB            -L{NCDF_F_LIB} -lnetcdff -L{NCDF_C_LIB} -lnetcdf \
                     -L{HDF5_LIB} -lhdf5_hl -lhdf5 -lz
%XIOS_INC            -I{XIOS_INC}
%XIOS_LIB            -L{XIOS_LIB} -lxios -lstdc++

%CPP                 cpp -Dkey_nosignedzero
%FC                  {MPIFC} -c -cpp
%FCFLAGS             {FFLAGS}
%FFLAGS              %FCFLAGS
%LD                  {LD} {LIBCXX}
%LDFLAGS
%FPPFLAGS            -P -C -traditional
%AR                  ar
%ARFLAGS             rs
%MK                  make
%USER_INC            %XIOS_INC %NCDF_INC
%USER_LIB            %XIOS_LIB %NCDF_LIB

%CC                  cc
%CFLAGS              -O0
""".format(
            **param
        )

        with open(file, "w") as f:
            f.write(text)

    def setup_run_environment(self, env):
        env.prepend_path("LD_LIBRARY_PATH", self.spec["netcdf-c"].prefix.lib)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["netcdf-fortran"].prefix.lib)

    def install(self, spec, prefix):
        self.nemo_fcm()
        install_tree(".", prefix)
