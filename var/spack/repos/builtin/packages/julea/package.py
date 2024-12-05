# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Julea(MesonPackage):
    """JULEA is a flexible storage framework that allows offering arbitrary
    I/O interfaces to applications. To be able to rapidly prototype new
    approaches, it offers object, key-value and database backends. Support
    for popular storage technologies such as POSIX, LevelDB and MongoDB is
    already included."""

    homepage = "https://github.com/wr-hamburg/julea"
    git = "https://github.com/wr-hamburg/julea.git"

    tags = ["HPC", "I/O", "storage"]
    maintainers("michaelkuhn")

    license("LGPL-3.0-or-later")

    version("master", branch="master")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("hdf5", default=True, description="Enable HDF5 support")
    variant("leveldb", default=True, description="Enable LevelDB support")
    variant("lmdb", default=True, description="Enable LMDB support")
    variant("mariadb", default=True, description="Enable MariaDB support")
    variant("mongodb", default=True, description="Enable MongoDB support")
    variant("rocksdb", default=True, description="Enable RocksDB support")
    variant("sqlite", default=True, description="Enable SQLite support")

    depends_on("pkgconfig", type="build")

    depends_on("glib")
    depends_on("libbson")
    # depends_on('libfabric')

    depends_on("hdf5@1.12.0:", when="+hdf5")
    depends_on("leveldb", when="+leveldb")
    depends_on("lmdb", when="+lmdb")
    depends_on("mariadb-c-client", when="+mariadb")
    depends_on("mongo-c-driver", when="+mongodb")
    depends_on("rocksdb", when="+rocksdb")
    depends_on("sqlite", when="+sqlite")
