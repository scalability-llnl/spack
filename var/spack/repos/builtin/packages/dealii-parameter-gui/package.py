# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class DealiiParameterGui(CMakePackage):
    """A qt based graphical user interface for editing deal.II .prm parameter
    files."""

    homepage = "https://github.com/dealii/parameter_gui"
    git = "https://github.com/dealii/parameter_gui.git"

    license("LGPL-2.1-or-later")

    version("develop", branch="master")

    depends_on("cxx", type="build")  # generated

    depends_on("qt")

    def setup_run_environment(self, env):
        env.set("PARAMETER_GUI_DIR", self.prefix)
