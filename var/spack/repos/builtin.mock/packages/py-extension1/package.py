# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path

from spack.package import *


class PyExtension1(PythonPackage):
    """A package which extends python"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/extension1-1.0.tar.gz"

    maintainers("user1", "user2")

    version("1.0", md5="00000000000000000000000000000110")
    version("2.0", md5="00000000000000000000000000000120")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with open(os.path.join(prefix.bin, "py-extension1"), "w+") as fout:
            fout.write(str(spec.version))

    extends("python")
