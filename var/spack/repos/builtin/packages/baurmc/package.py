# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Baurmc(AutotoolsPackage):
    """Baur's Monte Carlo package for simulating W+ gamma production at hadron
    colliders provides full electroweak calculation upto O(alpha) and contains
    higher order QCD corrections as well."""

    homepage = "https://twiki.cern.ch/twiki/bin/view/Sandbox/BaurMCInteface"
    url = "http://lcgpackages.web.cern.ch/lcgpackages/tarFiles/sources/MCGeneratorsTarFiles/baurmc-1.0-src.tgz"

    tags = ["hep"]

    maintainers("vvolkl")

    version("1.0", sha256="de5027ed2e66028bed890760bee9d869e1e330ac7f7112ee5cb25868cea5c35b")

    depends_on("fortran", type="build")  # generated

    @property
    def configure_directory(self):
        return os.path.join(self.stage.source_path, str(self.spec.version))

    def patch(self):
        filter_file("FC=g77", "FC=gfortran", str(self.spec.version) + "/configure", string=True)

    def configure_args(self):
        return [
            "--userfflags=-fno-automatic",
            "--userfflags=-fallow-argument-mismatch",
            "--enable-shared",
        ]

    def install(self, spec, prefix):
        build_libdir = os.path.join(str(spec.version), "lib")
        install_tree(build_libdir, self.prefix.lib)
