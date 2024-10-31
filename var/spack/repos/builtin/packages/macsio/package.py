# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Macsio(CMakePackage):
    """A Multi-purpose, Application-Centric, Scalable I/O Proxy Application."""

    tags = ["proxy-app", "ecp-proxy-app"]

    homepage = "https://computing.llnl.gov/projects/co-design/macsio"
    url = "https://github.com/LLNL/MACSio/archive/v1.1.tar.gz"
    git = "https://github.com/LLNL/MACSio.git"

    version("develop", branch="master")

    version("1.1", sha256="a86249b0f10647c0b631773db69568388094605ec1a0af149d9e61e95e6961ec")
    version("1.0", sha256="1dd0df28f9f31510329d5874c1519c745b5c6bec12e102cea3e9f4b05e5d3072")

    depends_on("c", type="build")  # generated

    variant("mpi", default=True, description="Build MPI plugin")
    variant("silo", default=False, description="Build with SILO plugin")
    # TODO: multi-level variants for hdf5
    variant("hdf5", default=False, description="Build HDF5 plugin")
    variant("zfp", default=False, description="Build HDF5 with ZFP compression")
    variant("szip", default=False, description="Build HDF5 with SZIP compression")
    variant("zlib", default=False, description="Build HDF5 with ZLIB compression")
    variant("pdb", default=False, description="Build PDB plugin")
    variant("exodus", default=False, description="Build EXODUS plugin")
    variant("scr", default=False, description="Build with SCR support")
    variant("typhonio", default=False, description="Build TYPHONIO plugin")

    depends_on("json-cwx")
    depends_on("mpi", when="+mpi")
    depends_on("silo", when="+silo")
    depends_on("hdf5+hl", when="+hdf5")
    # depends_on('hdf5+szip', when="+szip")
    depends_on("exodusii", when="+exodus")
    # pdb is packaged with silo
    depends_on("silo", when="+pdb")
    depends_on("typhonio", when="+typhonio")
    depends_on("scr", when="+scr")
    # macsio@1.1 has bug with ~mpi configuration
    conflicts("~mpi", when="@1.1")

    # Ref: https://github.com/LLNL/MACSio/commit/51b8c40cd9813adec5dd4dd6cee948bb9ddb7ee1
    patch("cast.patch", when="@1.1")

    def cmake_args(self):
        spec = self.spec
        cmake_args = []

        if "~mpi" in spec:
            cmake_args.append("-DENABLE_MPI=OFF")

        if "~silo" in spec:
            cmake_args.append("-DENABLE_SILO_PLUGIN=OFF")

        if "+silo" in spec:
            cmake_args.append("-DWITH_SILO_PREFIX={0}".format(spec["silo"].prefix))

        if "+pdb" in spec:
            # pdb is a part of silo
            cmake_args.append("-DENABLE_PDB_PLUGIN=ON")
            cmake_args.append("-DWITH_SILO_PREFIX={0}".format(spec["silo"].prefix))
        if "+hdf5" in spec:
            cmake_args.append("-DENABLE_HDF5_PLUGIN=ON")
            cmake_args.append("-DWITH_HDF5_PREFIX={0}".format(spec["hdf5"].prefix))
            # TODO: Multi-level variants
            # ZFP not in hdf5 spack package??
            # if "+zfp" in spec:
            #     cmake_args.append("-DENABLE_HDF5_ZFP")
            #     cmake_args.append("-DWITH_ZFP_PREFIX={0}"
            #         .format(spec['silo'].prefix))
            # SZIP is an hdf5 spack variant
            # if "+szip" in spec:
            #     cmake_args.append("-DENABLE_HDF5_SZIP")
            #     cmake_args.append("-DWITH_SZIP_PREFIX={0}"
            #         .format(spec['SZIP'].prefix))
            # ZLIB is on by default, @1.1.2
            # if "+zlib" in spec:
            #     cmake_args.append("-DENABLE_HDF5_ZLIB")
            #     cmake_args.append("-DWITH_ZLIB_PREFIX={0}"
            #         .format(spec['silo'].prefix))

        if "+typhonio" in spec:
            cmake_args.append("-DENABLE_TYPHONIO_PLUGIN=ON")
            cmake_args.append("-DWITH_TYPHONIO_PREFIX={0}".format(spec["typhonio"].prefix))

        if "+exodus" in spec:
            cmake_args.append("-DENABLE_EXODUS_PLUGIN=ON")
            cmake_args.append("-DWITH_EXODUS_PREFIX={0}".format(spec["exodusii"].prefix))
            # exodus requires netcdf
            cmake_args.append("-DWITH_NETCDF_PREFIX={0}".format(spec["netcdf-c"].prefix))

        return cmake_args
