# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RHdf5r(RPackage):
    """Interface to the 'HDF5' Binary Data Format.

    'HDF5' is a data model, library and file format for storing and managing
    large amounts of data. This package provides a nearly feature complete,
    object oriented wrapper for the 'HDF5' API
    <https://support.hdfgroup.org/HDF5/doc/RM/RM_H5Front.html> using R6
    classes. Additionally, functionality is added so that 'HDF5' objects behave
    very similar to their corresponding R counterparts."""

    cran = "hdf5r"

    license("Apache-2.0 OR custom")

    version("1.3.11", sha256="9795d667bc72acfabece1e3ece1aa4e60e8194cb4eb8b46985efccd19a55a8c4")
    version("1.3.8", sha256="b53281e2cf57447965849748e972de2f7fe8df0cee3538ef5813c33c7ed2302b")
    version("1.3.7", sha256="6e8a02843ed1c970cb41f97e2acee34853d3b70ce617bc9bcff07c41b98f295b")
    version("1.3.5", sha256="87b75173ab226a9fbaa5b28289349f3c56b638629560a172994b8f9323c1622f")
    version("1.3.3", sha256="a0f83cbf21563e81dbd1a1bd8379623ed0c9c4df4e094c75013abfd7a5271545")
    version("1.2.0", sha256="58813e334fd3f9040038345a7186e5cb02090898883ac192477a76a5b8b4fe81")

    depends_on("r@3.2.2:", type=("build", "run"))
    depends_on("r-r6", type=("build", "run"))
    depends_on("r-bit64", type=("build", "run"))
    depends_on("hdf5@1.8.13:+hl")
    depends_on("pkgconfig", type="build")

    # The configure script in the package uses the hdf5 h5cc compiler wrapper
    # in the PATH to configure hdf5. That works fine if hdf5 was built with
    # autotools but the hdf5 package in Spack is built with cmake. The compiler
    # wrapper built with cmake does not support the '-show' or '-showconfig'
    # flags. The following patch replaces those commands in the configure
    # script with pkg-config commands.
    patch("configure.patch", when="@:1.3.7")
