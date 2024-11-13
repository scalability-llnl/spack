# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ntirpc(CMakePackage):
    """New development on tirpc"""

    homepage = "https://github.com/nfs-ganesha/ntirpc"
    url = "https://github.com/nfs-ganesha/ntirpc/archive/v3.2.tar.gz"

    version("3.2", sha256="db1639ca2f15df7e30d8c0a820ed9adf4eb623798db03b56a3659eedff49af76")
    version("3.1", sha256="280b57db3a37c5b05116a7850460152b1ac53c050fd61ce190f5a5eb55ed3ba1")
    version("3.0", sha256="9a6b11c1aa3e7f5f1f491bca0275e759de5bed2d73c8a028af7b6aadb68ac795")
    version("1.8.0", sha256="3bb642dccc8f2506b57a03b5d3358654f59f47b33fddfaa5a7330df4cf336f9f")
    version("1.7.3", sha256="8713ef095efc44df426bbd2b260ad457e5335bf3008fb97f01b0775c8042e54b")

    depends_on("c", type="build")  # generated

    depends_on("libnsl")
    depends_on("userspace-rcu")
