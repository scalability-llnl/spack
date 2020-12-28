# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RHdf5r(RPackage):
    """'HDF5' is a data model, library and file format for storing and managing
    large amounts of data. This package provides a nearly feature complete,
    object oriented wrapper for the 'HDF5' API
    <https://support.hdfgroup.org/HDF5/doc/RM/RM_H5Front.html> using R6
    classes. Additionally, functionality is added so that 'HDF5' objects behave
    very similar to their corresponding R counterparts."""

    homepage = "https://hhoeflin.github.io/hdf5r"
    url      = "https://cloud.r-project.org/src/contrib/hdf5r_1.2.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/hdf5r"

    version('1.2.0', sha256='58813e334fd3f9040038345a7186e5cb02090898883ac192477a76a5b8b4fe81')

    depends_on('r@3.2.2:', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
    depends_on('r-bit64', type=('build', 'run'))
    depends_on('hdf5@1.8.13:')

    def configure_args(self):
        if 'mpi' in self.spec:
            args = [
                '--with-hdf5={0}/h5pcc'.format(self.spec['hdf5'].prefix.bin),
            ]
        else:
            args = [
                '--with-hdf5={0}/h5cc'.format(self.spec['hdf5'].prefix.bin),
            ]
        return args
