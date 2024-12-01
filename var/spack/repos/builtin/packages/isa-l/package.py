# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class IsaL(AutotoolsPackage):
    """ISA-L is a collection of optimized low-level functions targeting
    storage applications. ISA-L includes:

    - Erasure codes - Fast block Reed-Solomon type erasure codes for
      any encode/decode matrix in GF(2^8).
    - CRC - Fast implementations of cyclic redundancy check. Six
      different polynomials supported.
        iscsi32, ieee32, t10dif, ecma64, iso64, jones64.
    - Raid - calculate and operate on XOR and P+Q parity found in
      common RAID implementations.
    - Compression - Fast deflate-compatible data compression.
    - De-compression - Fast inflate-compatible data compression.
    """

    homepage = "https://github.com/intel/isa-l"
    url = "https://github.com/intel/isa-l/archive/v2.25.0.tar.gz"
    git = "https://github.com/intel/isa-l.git"
    maintainers("hyoklee")

    license("BSD-3-Clause")

    version("master", branch="master")

    # Current
    version("2.30.0", sha256="bcf592c04fdfa19e723d2adf53d3e0f4efd5b956bb618fed54a1108d76a6eb56")
    version("2.29.0", sha256="832d9747ef3f0c8c05d39e3d7fd6ee5299a844e1ee7382fc8c8b52a268f36eda")
    version("2.28.0", sha256="589202efdcfe437b1786750ec81bf93055e3b88a4bdf909d3b519f2a7134034b")
    version("2.27.0", sha256="d398c5072e8e73bebf02ad4f1db3c13e27a7d96c8c1630e75a19c9bd79a92964")
    version("2.26.0", sha256="938ccce1764ed8fb65a13b02295be5af9a5e0d91686efb7474bde666214153b3")
    version("2.25.0", sha256="302bb38bf76be632dbd338ab97efe1c84d47dbe6265ff7af8cb373f256c84b48")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("yasm@1.2.0:", type="build")
    depends_on("nasm@2.13:", type="build")

    def configure_args(self):
        config_args = ["--enable-shared"]

        return config_args
