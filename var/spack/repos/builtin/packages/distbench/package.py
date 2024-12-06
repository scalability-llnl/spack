# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Distbench(MakefilePackage):
    """Distbench is a tool for synthesizing a variety of network traffic patterns used in
    distributed systems, and evaluating their performance across multiple networking stacks."""

    homepage = "https://github.com/google/distbench"
    url = "https://github.com/google/distbench/archive/refs/tags/v1.0rc4.tar.gz"

    license("Apache-2.0")

    version("1.0rc4", sha256="adc8da85890219800207d0d4cd7ffd63193d2c4007dba7c44cf545cc13675ff7")

    depends_on("cxx", type="build")  # generated

    depends_on("bazel", type="build")

    def patch(self):
        filter_file("bazel build", f"bazel build --jobs={make_jobs}", "Makefile", string=True)
