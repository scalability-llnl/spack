# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Redis(MakefilePackage):
    """Redis is an open source (BSD licensed), in-memory data structure store,
    used as a database, cache and message broker.

    It supports data structures such as strings, hashes, lists, sets, sorted
    sets with range queries, bitmaps, hyperloglogs, geospatial indexes with
    radius queries and streams. Redis has built-in replication, Lua scripting,
    LRU eviction, transactions and different levels of on-disk persistence,
    and provides high availability via Redis Sentinel and automatic
    partitioning with Redis Cluster
    """

    homepage = "https://redis.io"
    url = "http://download.redis.io/releases/redis-5.0.3.tar.gz"

    version('5.0.3',   sha256='e290b4ddf817b26254a74d5d564095b11f9cd20d8f165459efa53eb63cd93e02')
    version('5.0.2',   sha256='937dde6164001c083e87316aa20dad2f8542af089dfcb1cbb64f9c8300cd00ed')
    version('5.0.1',   sha256='82a67c0eec97f9ad379384c30ec391b269e17a3e4596393c808f02db7595abcb')
    version('5.0.0',   sha256='70c98b2d0640b2b73c9d8adb4df63bcb62bad34b788fe46d1634b6cf87dc99a4')
    version('4.0.13',  sha256='17d955227966dcd68590be6139e5fe7f2d19fc4fb7334248a904ea9cdd30c1d4')
    version('4.0.12',  sha256='6447259d2eed426a949c9c13f8fdb2d91fb66d9dc915dd50db13b87f46d93162')
    version('4.0.11',  sha256='fc53e73ae7586bcdacb4b63875d1ff04f68c5474c1ddeda78f00e5ae2eed1bbb')

    @property
    def install_targets(self):
        return [
            'PREFIX={0}'.format(self.spec.prefix),
            'install'
        ]

    @run_after('install')
    def install_conf(self):
        mkdirp(self.prefix.conf)
        install('redis.conf', self.prefix.conf)
