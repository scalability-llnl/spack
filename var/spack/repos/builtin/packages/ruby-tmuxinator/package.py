# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyTmuxinator(RubyPackage):
    """Create and manage complex tmux sessions easily."""

    homepage = "https://github.com/tmuxinator/tmuxinator"
    url = "https://github.com/tmuxinator/tmuxinator/archive/v2.0.1.tar.gz"

    license("MIT")

    version("2.0.1", sha256="a2c8428d239a6e869da516cecee3ac64db47ba1f1932317eb397b1afd698ee09")

    depends_on("ruby@2.5.8:", type=("build", "run"))
    depends_on("ruby-erubis@2.6:2", type=("build", "run"))
    depends_on("ruby-thor@1.0:1", type=("build", "run"))
    depends_on("ruby-xdg@2.2.5:2", type=("build", "run"))
