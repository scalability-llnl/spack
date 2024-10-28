# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Lazygit(GoPackage):
    """A simple terminal UI for git commands"""

    homepage = "https://github.com/jesseduffield/lazygit"
    url = "https://github.com/jesseduffield/lazygit/archive/refs/tags/v0.40.2.tar.gz"

    maintainers("twrs")

    license("MIT")

    version("0.44.1", sha256="02b67d38e07ae89b0ddd3b4917bd0cfcdfb5e158ed771566d3eb81f97f78cc26")
    version("0.41.0", sha256="f2176fa253588fe4b7118bf83f4316ae3ecb914ae1e99aad8c474e23cea49fb8")
    version("0.40.2", sha256="146bd63995fcf2f2373bbc2143b3565b7a2be49a1d4e385496265ac0f69e4128")

    depends_on("go@1.20:", type="build", when="@0.40:")
    depends_on("go@1.21:", type="build", when="@0.41:")
    depends_on("go@1.22:", type="build", when="@0.42:")
