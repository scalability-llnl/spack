# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Adf(Package):
    """Amsterdam Density Functional (ADF) is a program for first-principles
    electronic structure calculations that makes use of density functional
    theory."""

    homepage = "https://www.scm.com/product/adf/"
    manual_download = True

    version("2017.113", sha256="666ef15d253b74c707dd14da35e7cf283ca20e21e24ed43cb953fb9d1f2f1e15")

    def url_for_version(self, version):
        return f"file://{os.getcwd()}/adf/adf{version}.pc64_linux.openmpi.bin.tgz"

    # Licensing
    license_required = True
    license_files = ["license.txt"]
    license_vars = ["SCMLICENSE"]

    def setup_run_environment(self, env):
        env.set("ADFHOME", self.prefix)
        env.set("ADFBIN", self.prefix.bin)
        env.set("ADFRESOURCES", self.prefix.atomicdata)
        env.set("SCMLICENSE", join_path(self.prefix, "license.txt"))
        env.set("SCM_TMPDIR", "/tmp")

    def install(self, spec, prefix):
        install_tree(".", prefix)
