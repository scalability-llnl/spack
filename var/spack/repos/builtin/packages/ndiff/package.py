# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ndiff(Package):
    """The ndiff tool is a binary utility that compares putatively similar
    files while ignoring small numeric differernces. This utility is
    most often used to compare files containing a lot of
    floating-point numeric data that may be slightly different due to
    numeric error.

    """

    homepage = "https://ftp.math.utah.edu/pub/ndiff/"
    url = "https://ftp.math.utah.edu/pub/ndiff/ndiff-2.00.tar.gz"

    license("GPL-2.0-only")

    version("2.00", sha256="f2bbd9a2c8ada7f4161b5e76ac5ebf9a2862cab099933167fe604b88f000ec2c")
    version("1.00", sha256="d4be3ab38e4b87da8d689fe47413e01a7bfdf8c8627bfb673aac37953a463a92")

    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        mkdirp(prefix.bin)
        mkdirp("%s/lib" % prefix.share)

        make("install-exe", "install-shrlib")
