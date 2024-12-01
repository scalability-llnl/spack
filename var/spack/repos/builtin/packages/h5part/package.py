# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class H5part(AutotoolsPackage):
    """Portable High Performance Parallel Data Interface to HDF5"""

    homepage = "https://dav.lbl.gov/archive/Research/AcceleratorSAPP/"
    url = "https://codeforge.lbl.gov/frs/download.php/latestfile/18/H5Part-1.6.6.tar.gz"

    version("1.6.6", sha256="10347e7535d1afbb08d51be5feb0ae008f73caf889df08e3f7dde717a99c7571")
    patch("mpiio.patch")

    depends_on("mpi")
    depends_on("hdf5+mpi")

    def configure_args(self):
        args = [
            "--enable-parallel",
            "--with-hdf5=%s" % self.spec["hdf5"].prefix,
            "CC=mpicc",
            "CXX=mpicxx",
        ]
        return args
