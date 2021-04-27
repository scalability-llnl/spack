# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""An environment analyzer will read and parse the environment variables
file in the installed package directory, generating a json file that has
an index of key, value pairs for environment variables."""


from .analyzer_base import AnalyzerBase
from spack.util.environment import EnvironmentModifications


import os


class EnvironmentVariables(AnalyzerBase):

    name = "environment_variables"
    outfile = "spack-analyzer-environment-variables.json"
    description = "environment variables parsed from spack-build-env.txt"

    def run(self):
        """
        Load, parse, and save spack-build-env.txt to analyzers.

        Read in the spack-build-env.txt file from the package install
        directory and parse the environment variables into key value pairs.
        The result should have the key for the analyzer, the name.
        """
        env_file = os.path.join(self.meta_dir, "spack-build-env.txt")
        return {self.name: self._read_environment_file(env_file)}

    def _read_environment_file(self, filename):
        """
        Read and parse the environment file.

        Given an environment file, we want to read it, split by semicolons
        and new lines, and then parse down to the subset of SPACK_* variables.
        We assume that all spack prefix variables are not secrets, and unlike
        the install_manifest.json, we don't (at least to start) parse the values
        to remove path prefixes specific to user systems.
        """
        if not os.path.exists(filename):
            return

        mods = EnvironmentModifications.from_sourcing_file(filename)
        env = {}
        mods.apply_modifications(env)
        return env
