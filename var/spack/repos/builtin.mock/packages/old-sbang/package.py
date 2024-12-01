# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.paths
import spack.store
from spack.package import *


class OldSbang(Package):
    """Toy package for testing the old sbang replacement problem"""

    homepage = "https://www.example.com"
    url = "https://www.example.com/old-sbang.tar.gz"

    version("1.0.0", md5="0123456789abcdef0123456789abcdef")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

        sbang_style_1 = """#!/bin/bash {0}/bin/sbang
#!/usr/bin/env python

{1}
""".format(
            spack.paths.prefix, prefix.bin
        )
        sbang_style_2 = """#!/bin/sh {0}/bin/sbang
#!/usr/bin/env python

{1}
""".format(
            spack.store.STORE.unpadded_root, prefix.bin
        )
        with open("%s/sbang-style-1.sh" % self.prefix.bin, "w") as f:
            f.write(sbang_style_1)

        with open("%s/sbang-style-2.sh" % self.prefix.bin, "w") as f:
            f.write(sbang_style_2)
