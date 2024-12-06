# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ModulePathSeparator(Package):
    homepage = "http://www.llnl.gov"
    url = "http://www.llnl.gov/module-path-separator-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    def setup_run_environment(self, env):
        env.append_path("COLON", "foo")
        env.prepend_path("COLON", "foo")
        env.remove_path("COLON", "foo")

        env.append_path("SEMICOLON", "bar", separator=";")
        env.prepend_path("SEMICOLON", "bar", separator=";")
        env.remove_path("SEMICOLON", "bar", separator=";")

        env.append_flags("SPACE", "qux")
        env.remove_flags("SPACE", "qux")
