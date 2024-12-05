# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Hibench(MavenPackage):
    """HiBench is a big data benchmark suite that helps evaluate different big
    data frameworks in terms of speed, throughput and system resource
    utilizations. It contains a set of Hadoop,Spark and streaming workloads,
    including Sort, WordCount, TeraSort, Repartition, Sleep, SQL,PageRank,
    Nutch indexing, Bayes, Kmeans, NWeight and enhanced DFSIO, etc."""

    homepage = "https://github.com/Intel-bigdata/HiBench"
    url = "https://github.com/Intel-bigdata/HiBench/archive/HiBench-7.1.tar.gz"

    license("Apache-2.0")

    version("7.1", sha256="96572a837d747fb6347f2b906fd5f7fb97a62095435326ccfee5e75777a5c210")
    version("7.0", sha256="89b01f3ad90b758f24afd5ea2bee997c3d700ce9244b8a2b544acc462ab0e847")
    version("6.0", sha256="179f5415903f4029bd0ea1101a3d4c67faf88ca46a993d8179582299ad730f79")
    version("5.0", sha256="32d6a7bc1010d90b2f22906896a03cd1980e617beb07b01716e3d04de5760ed4")
    version("4.1", sha256="07551763aa30f04d32870c323524b5fc0fc2e968d7081d8916575bdeb4fd1381")
    version("4.0", sha256="de58ed5e9647ffe28c2a905a8830b661bbd09db334eb5b3472c8186553407e0e")
    version("3.0.0", sha256="869771e73593caac3a9b2fb14a10041a485d248074ba38cca812c934897db63d")
    version("2.2.1", sha256="f8531cbaff8d93bfd1c0742fec5dbb375bfeeb9ec1b39b4e857120e933a2c9ec")
    version("2.2", sha256="5f68e22339cdd141b846d8b1d7134b2b8ff5fbd5e847e406214dc845f5d005cf")
