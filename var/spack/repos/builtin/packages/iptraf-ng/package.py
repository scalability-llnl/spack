# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class IptrafNg(MakefilePackage):
    """A console-based network monitoring utility."""

    homepage = "https://github.com/iptraf-ng/iptraf-ng"
    url = "https://github.com/iptraf-ng/iptraf-ng/archive/v1.2.0.tar.gz"

    license("GPL-2.0-only")

    version("1.2.1", sha256="9f5cef584065420dea1ba32c86126aede1fa9bd25b0f8362b0f9fd9754f00870")
    version("1.2.0", sha256="9725115e501d083674d50a7686029d3a08f920abd35c9a2d4a28b5ddb782417f")
    version("1.1.4", sha256="16b9b05bf5d3725d86409b901696639ad46944d02de6def87b1ceae5310dd35c")

    depends_on("c", type="build")  # generated

    depends_on("ncurses")

    def install(self, spec, prefix):
        make("install", "prefix={0}".format(prefix))
