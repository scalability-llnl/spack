# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyTerminalTable(RubyPackage):
    """Simple, feature rich ascii table generation library"""

    homepage = "https://github.com/tj/terminal-table"
    url = "https://github.com/tj/terminal-table/archive/v1.8.0.tar.gz"

    license("MIT")

    version("1.8.0", sha256="69b8e157f5dc3f056b5242923ab3e729a16c6f893b3a5d540e71135a973e5fbe")

    depends_on("ruby-unicode-display-width@1.1.1:1", type=("build", "run"))
