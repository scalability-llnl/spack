# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ltp(AutotoolsPackage):
    """Ltp is a joint project started by SGI, developed and maintained by IBM,
    Cisco, Fujitsu, SUSE, Red Hat and others, that has a goal to deliver
    test suites to the open source community that validate the reliability,
    robustness,and stability of Linux. The LTP testsuite contains a collection
    of tools for testing the Linux kernel and related features."""

    homepage = "https://github.com/linux-test-project/ltp"
    url = "https://github.com/linux-test-project/ltp/archive/20190517.tar.gz"

    license("GPL-2.0-only")

    version("20230516", sha256="6f2578fa1687093acf615544ab5ea814b792461bd314c79738bac4d511e3a10c")
    version("20230127", sha256="ecefb6147dff5abd821a7f621ec2845ade22b8adf3022c0a451f79ecd02ab6f7")
    version("20190930", sha256="eca11dbe11a61f3035561a2aa272d578ca9380563440f9ba876c0c4755a42533")
    version("20190517", sha256="538175fff2d6c9d69748b2d4afcf5ac43f7300456f839fa7b5b101c7ad447af7")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
