# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tajo(Package):
    """
    Tajo is a relational and distributed data warehouse system for Hadoop
    Tajo is designed for low-latency and scalable ad-hoc queries, online
    aggregation and ETL on large-data sets by leveraging advanced database
    techniques. It supports SQL standards. It has its own query engine which
    allows direct control of distributed execution and data flow. As a result,
    Tajo has a variety of query evaluation strategies and more optimization
    opportunities. In addition, Tajo will have a native columnar execution
    and and its optimizer.
    """

    homepage = "https://tajo.apache.org/"
    url = "https://www-eu.apache.org/dist/tajo/tajo-0.11.3/tajo-0.11.3.tar.gz"
    list_url = "https://www-eu.apache.org/dist/tajo/"
    list_depth = 1

    version("0.11.3", sha256="9be736f13575aefc68f94eff376ef284ca3af8b0bdceb6d9d825980bb10a44e8")
    version("0.11.2", sha256="8a7a5b63b799cd3db275f3a3e265063594c60ec6b8ca394bf2c88b1d1867779f")
    version("0.11.1", sha256="723a2bf02c1109652aabc5786b087634dcca014083569d368a9d4ce118d87b91")
    version("0.11.0", sha256="0714b4c49afdd40010f9d1af9443a2a38453157f6352abd908da6ebfafa8abca")
    version("0.10.1", sha256="754bd6d34fd4ed1b142d50b9025747167c3fbf819ee04711aca8d8842a53a625")
    version("0.10.0", sha256="66e56ac5948e01779d9bf14f9a3f8145dec9ed3273b84dd66d9f08d581dad433")

    depends_on("java", type="run")

    def install(self, spec, prefix):
        install_tree(".", prefix)
