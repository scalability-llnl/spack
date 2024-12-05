# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class AutotoolsConfigReplacement(AutotoolsPackage):
    """
    This package features broken and working config.sub and config.guess files,
    that should be replaced by the ones provided by gnuconfig. It allows testing
    with / without patches and with / without substitutes available.
    """

    has_code = False

    version("1.0.0")
    variant("patch_config_files", default=False)
    variant("gnuconfig", default=False)

    depends_on("gnuconfig", type="build", when="+gnuconfig")

    @property
    def patch_config_files(self):
        return self.spec.satisfies("+patch_config_files")

    def autoreconf(self, spec, prefix):
        pass

    def configure(self, spec, prefix):
        pass

    def build(self, spec, prefix):
        pass

    def install(self, spec, prefix):
        broken = os.path.join(self.stage.source_path, "broken")
        working = os.path.join(self.stage.source_path, "working")
        install_tree(broken, self.prefix.broken)
        install_tree(working, self.prefix.working)

    @run_before("autoreconf")
    def create_the_package_sources(self):
        # Creates the following file structure:
        # ./broken/config.sub    -- not executable
        # ./broken/config.guess  -- exectuable & exit code 1
        # ./working/config.sub   -- executable & exit code 0
        # ./working/config.guess -- executable & exit code 0
        # Automatic config helper script substitution should replace the two
        # broken scripts with those from the gnuconfig package.

        broken = os.path.join(self.stage.source_path, "broken")
        working = os.path.join(self.stage.source_path, "working")

        mkdirp(broken)
        mkdirp(working)

        # a configure script is required
        configure_script = join_path(self.stage.source_path, "configure")
        with open(configure_script, "w") as f:
            f.write("#!/bin/sh\nexit 0")
        os.chmod(configure_script, 0o775)

        # broken config.sub (not executable)
        broken_config_sub = join_path(broken, "config.sub")
        with open(broken_config_sub, "w") as f:
            f.write("#!/bin/sh\nexit 0")

        # broken config.guess (exectuable but with error return code)
        broken_config_guess = join_path(broken, "config.guess")
        with open(broken_config_guess, "w") as f:
            f.write("#!/bin/sh\nexit 1")
        os.chmod(broken_config_guess, 0o775)

        # working config.sub
        working_config_sub = join_path(working, "config.sub")
        with open(working_config_sub, "w") as f:
            f.write("#!/bin/sh\nexit 0")
        os.chmod(working_config_sub, 0o775)

        # working config.guess
        working_config_guess = join_path(working, "config.guess")
        with open(working_config_guess, "w") as f:
            f.write("#!/bin/sh\nexit 0")
        os.chmod(working_config_guess, 0o775)
