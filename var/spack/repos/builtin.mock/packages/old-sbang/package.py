# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.hooks.sbang import sbang_shebang_line
from spack.package import *


class OldSbang(Package):
    """Package for testing sbang relocation"""

    homepage = "https://www.example.com"
    url = "https://www.example.com/old-sbang.tar.gz"

    version("1.0.0", md5="0123456789abcdef0123456789abcdef")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        contents = f"""\
{sbang_shebang_line()}
#!/usr/bin/env python3

{prefix.bin}
"""
        with open(os.path.join(self.prefix.bin, "script.sh"), "w", encoding="utf-8") as f:
            f.write(contents)
