# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mpest(MakefilePackage):
    """MP-EST estimates species trees from a set of gene trees by maximizing
    a pseudo-likelihood function."""

    homepage = "http://faculty.franklin.uga.edu/lliu/content/mp-est"
    url = "https://faculty.franklin.uga.edu/lliu/sites/faculty.franklin.uga.edu.lliu/files/mpest_1.5.zip"

    version("1.5", sha256="536895120fc34b19b0740c7fef6467b74c284ae4f1f29c9f5fc5c633f30e4916")

    @property
    def build_directory(self):
        return join_path("mpest_{0}".format(self.version), "src")

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            mkdirp(prefix.bin)
            install("mpest", prefix.bin)

    def setup_build_environment(self, env):
        if self.spec.satisfies("platform=darwin"):
            env.set("ARCHITECTURE", "mac")
        else:
            env.set("ARCHITECTURE", "unix")
