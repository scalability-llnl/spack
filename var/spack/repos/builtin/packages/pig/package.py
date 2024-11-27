# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pig(Package):
    """
    Pig is a dataflow programming environment for processing very large files.
    Pig's language is called Pig Latin. A Pig Latin program consists of a
    directed acyclic graph where each node represents an operation that
    transforms data.
    """

    homepage = "https://archive.apache.org"
    url = "https://archive.apache.org/dist/hadoop/pig/stable/pig-0.7.0.tar.gz"

    license("Apache-2.0")

    version("0.7.0", sha256="fa7211fb339f547f679a3dd90055f1ddc45d5754d88463e4cc39c380ddf8b02a")

    def install(self, spec, prefix):
        install_tree(".", prefix)
