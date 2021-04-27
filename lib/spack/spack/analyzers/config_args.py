# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""A configargs analyzer is a class of analyzer that typically just uploads
already existing metadata about config args from a package spec install
directory."""


import spack.monitor
from .analyzer_base import AnalyzerBase

import os


class ConfigArgs(AnalyzerBase):

    name = "config_args"
    outfile = "spack-analyzer-config-args.json"
    description = "config args loaded from spack-configure-args.txt"

    def run(self):
        """
        Load the configure-args.txt and save in json.

        The run function will find the spack-config-args.txt file in the
        package install directory, and read it into a json structure that has
        the name of the analyzer as the key.
        """
        config_file = os.path.join(self.meta_dir, "spack-configure-args.txt")
        return {self.name: spack.monitor.read_file(config_file)}
