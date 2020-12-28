# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Librdkafka(AutotoolsPackage):
    """librdkafka is a C library implementation of the Apache Kafka
    protocol."""

    homepage = "https://github.com/edenhill/librdkafka"
    url      = "https://github.com/edenhill/librdkafka/archive/v1.5.0.tar.gz"

    version('1.5.0', 'f7fee59fdbf1286ec23ef0b35b2dfb41031c8727c90ced6435b8cf576f23a656')
    version('1.4.4', '0984ffbe17b9e04599fb9eceb16cfa189f525a042bef02474cd1bbfe1ea68416')
    version('1.4.2', '3b99a36c082a67ef6295eabd4fb3e32ab0bff7c6b0d397d6352697335f4e57eb')

    depends_on('zstd')
    depends_on('lz4')
