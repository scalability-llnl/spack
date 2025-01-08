# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path

from spack.package import *


class PerlExtension(PerlPackage):
    """A package which extends perl"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/extension1-1.0.tar.gz"

    version("1.0", md5="00000000000000000000000000000010")
    version("2.0", md5="00000000000000000000000000000020")

    extends("perl")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with open(os.path.join(prefix.bin, "perl-extension"), "w+", encoding="utf-8") as fout:
            fout.write(str(spec.version))
