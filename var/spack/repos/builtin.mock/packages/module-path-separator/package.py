# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ModulePathSeparator(Package):
    homepage = "http://www.llnl.gov"
    url      = "http://www.llnl.gov/module-path-separator-1.0.tar.gz"

    version(1.0, 'foobarbaz')

    def setup_environment(self, senv, renv):
        renv.append_path("COLON", "foo")
        renv.prepend_path("COLON", "foo")
        renv.remove_path("COLON", "foo")

        renv.append_path("SEMICOLON", "bar", separator=";")
        renv.prepend_path("SEMICOLON", "bar", separator=";")
        renv.remove_path("SEMICOLON", "bar", separator=";")
