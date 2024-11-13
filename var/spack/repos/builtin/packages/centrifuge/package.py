# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Centrifuge(MakefilePackage):
    """Classifier for metagenomic sequences."""

    homepage = "https://ccb.jhu.edu/software/centrifuge/index.shtml"
    url = "https://github.com/DaehwanKimLab/centrifuge/archive/refs/tags/v1.0.4.tar.gz"

    version("1.0.4.1", sha256="638cc6701688bfdf81173d65fa95332139e11b215b2d25c030f8ae873c34e5cc")
    version("1.0.4", sha256="929daed0f84739f7636cc1ea2757527e83373f107107ffeb5937a403ba5201bc")

    depends_on("cxx", type="build")  # generated

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        make("install", "prefix=" + prefix)
