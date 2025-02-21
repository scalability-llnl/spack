# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGert(RPackage):
    """Simple Git Client for R.

    Simple git client for R based on 'libgit2' with support for SSH and  HTTPS
    remotes. All functions in 'gert' use basic R data types (such as vectors
    and data-frames) for their arguments and return values. User credentials
    are shared with command line 'git' through the git-credential store and ssh
    keys stored on disk or ssh-agent."""

    cran = "gert"

    license("MIT")

    version("2.1.1", sha256="42037c041b284ae7ef4da68b784f2dfc3f72701534a8330265b1abc382eda964")
    version("1.9.2", sha256="42ca1b4bcafb1fdbbc7f54df0ee4476ecd19e9e7d563b53fe7064e0086ab665e")
    version("1.9.1", sha256="751d18760a08ae00b8de73dc3e564cf4e76b1f47c7179101320e1b70152e1fdd")
    version("1.6.0", sha256="8c440aeebabf1cb3b57124ec9280e0f46b2ab56f2bca07d72b5c7a7f4edc2964")
    version("1.5.0", sha256="9fc330893b0cb43360905fd204e674813e1906449a95dc4037fe8802bd74a2ae")
    version("1.0.2", sha256="36687ab98291d50a35752fcb2e734a926a6b845345c18d36e3f48823f68304d3")

    depends_on("r-askpass", type=("build", "run"))
    depends_on("r-credentials@1.2.1:", type=("build", "run"))
    depends_on("r-openssl@1.4.1:", type=("build", "run"))
    depends_on("r-openssl@2.0.3:", type=("build", "run"), when="@1.9.1:")
    depends_on("r-rstudioapi@0.11:", type=("build", "run"))
    depends_on("r-sys", type=("build", "run"), when="@1.5.0:")
    depends_on("r-zip@2.1.0:", type=("build", "run"))
    depends_on("libgit2@0.26:")
    depends_on("libgit2@1.0:", when="@1.6.0:")
