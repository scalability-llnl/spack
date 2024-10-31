# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libjson(MakefilePackage):
    """libjson is a simple library without any dependancies to parse and
    pretty print the JSON format (RFC 4627). The JSON format is a concise
    and structured data format."""

    homepage = "https://github.com/vincenthz/libjson"
    url = "https://github.com/vincenthz/libjson/archive/v0.8.tar.gz"

    version("0.8", sha256="a6ffcc2f8f649daa9a3247569bbc09e405b17e30b72da31418cc68d771265db6")
    version("0.7", sha256="6620213876706a784532b743e1a4dac5710356af2f5578ebccb408e67fd2456a")
    version("0.6", sha256="55a094343e8c0fafc2060b73ba5555022257cddf7ac173f6f6c439793a6119d5")
    version("0.5", sha256="d19e149118c01c4a1f4cd16be3ce54bfc97a7210b6f0d76a3f8ef75bf70e8acd")
    version("0.4", sha256="9b3ebbeb1940dbd8664524d27e66d991fedc00cca9f403f9aa9c2f28104ca81b")

    depends_on("c", type="build")  # generated

    def edit(self, spec, prefix):
        filter_file("-o root -g root", "", "Makefile")

    def install(self, spec, prefix):
        make("install", "PREFIX={0}".format(prefix))
