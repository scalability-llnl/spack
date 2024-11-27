# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class MongodbAsyncDriver(MavenPackage):
    """The MongoDB Asynchronous Java Driver."""

    homepage = "http://www.allanbank.com/mongodb-async-driver/"
    url = "https://github.com/allanbank/mongodb-async-driver/archive/rel_2.0.1.tar.gz"

    license("Apache-2.0")

    version("2.0.1", sha256="87f22c16f3744a847eeb8276ed132bf235f025db0b7dee0d0f239d5cdcab720c")
    version("2.0.0", sha256="8cffe4c960d42550be30c27d66f5de6df4edb5ee7a094c50519986dc5cbcf9b8")
