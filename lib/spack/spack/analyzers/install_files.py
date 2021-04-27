# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""The install files json file (install_manifest.json) already exists in
the package install folder, so this analyzer simply moves it to the user
analyzer folder for further processing."""


import spack.monitor
from .analyzer_base import AnalyzerBase

import os


class InstallFiles(AnalyzerBase):

    name = "install_files"
    outfile = "spack-analyzer-install-files.json"
    description = "install file listing read from install_manifest.json"

    def run(self):
        """
        Load in the install_manifest.json and save to analyzers.

        We write it out to the analyzers folder, with key as the analyzer name.
        """
        manifest_file = os.path.join(self.meta_dir, "install_manifest.json")
        return {self.name: spack.monitor.read_json(manifest_file)}
