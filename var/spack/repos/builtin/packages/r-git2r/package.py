# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGit2r(RPackage):
    """Provides Access to Git Repositories.

    Interface to the 'libgit2' library, which is a pure C implementation of the
    'Git' core methods. Provides access to 'Git' repositories to extract data
    and running some basic 'Git' commands."""

    cran = "git2r"

    license("GPL-2.0-only")

    version("0.33.0", sha256="1855b68d0e22566f1c255fdcb8e13282a2bebf55cbc804a8591dc8047f0e1895")
    version("0.32.0", sha256="1b5d254c0c684a56751d26d482823d0006964eb1f55c558f365d037f5e984671")
    version("0.31.0", sha256="f1db9278fa4604600a64beaedcf86dda595d7c8a10cdb1f7300a6635e73cd66d")
    version("0.30.1", sha256="85d913ddc7659e32c1b98ebc247fa1cc1b7717a5bd413fa78ea84696986ca840")
    version("0.29.0", sha256="f8f7a181dc0ac761f2a0c4099bfd744ded01c0e0832cab32dc5b4da32accd48e")
    version("0.28.0", sha256="ce6d148d21d2c87757e98ef4474b2d09faded9b9b866f046bd26d4ca925e55f2")
    version("0.27.1", sha256="099207f180aa45ddcc443cbb22487eafd14e1cd8e5979b3476214253fd773bc0")
    version("0.26.1", sha256="13d609286a0af4ef75ba76f2c2f856593603b8014e311b88896243a50b417435")
    version("0.26.0", sha256="56671389c3a50591e1dae3be8c3b0112d06d291f897d7fe14db17aea175616cf")
    version("0.18.0", sha256="91b32e49afb859c0c4f6f77988343645e9499e5046ef08d945d4d8149b6eff2d")
    version("0.15.0", sha256="682ab9e7f71b2ed13a9ef95840df3c6b429eeea070edeb4d21d725cf0b72ede6")

    depends_on("r@3.1:", type=("build", "run"))
    depends_on("r@3.4:", type=("build", "run"), when="@0.31.0:")
    depends_on("r@4.0:", type=("build", "run"), when="@0.33.0:")
    depends_on("libgit2")
    depends_on("zlib-api")
    depends_on("openssl")
    depends_on("libssh2")
