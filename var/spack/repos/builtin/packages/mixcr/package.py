# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mixcr(Package):
    """MiXCR is a universal framework that processes big immunome data from
    raw sequences to quantitated clonotypes. MiXCR efficiently handles
    paired- and single-end reads, considers sequence quality, corrects PCR
    errors and identifies germline hypermutations. The software supports
    both partial- and full-length profiling and employs all available RNA or
    DNA information, including sequences upstream of V and downstream of J
    gene segments."""

    homepage = "https://mixcr.readthedocs.io/en/master/index.html"
    url = "https://github.com/milaboratory/mixcr/releases/download/v3.0.2/mixcr-3.0.2.zip"

    version("4.6.0", sha256="05db1276951a2e656d0a7bf4e2b1fff326733a5f961a9d4829be139852fabe13")
    version("4.3.2", sha256="8f67cda8e55eeee66b46db0f33308418b6ddb63ca8914623035809ccb5aae2c2")
    version("3.0.2", sha256="b4dcad985053438d5f5590555f399edfbd8cb514e1b9717620ee0ad0b5eb6b33")

    depends_on("java@8:")

    def install(self, spec, prefix):
        install_tree(".", prefix)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix)
