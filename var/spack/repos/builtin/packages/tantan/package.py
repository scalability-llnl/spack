# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tantan(MakefilePackage):
    """tantan is a tool to mask simple regions (low complexity and
    short-period tandem repeats) in DNA, RNA, and protein sequences."""

    homepage = "http://cbrc3.cbrc.jp/~martin/tantan"
    url = "http://cbrc3.cbrc.jp/~martin/tantan/tantan-13.zip"

    license("GPL-3.0-only")

    version("13", sha256="3f7ba7d8d04a32c3716ea3e4e2f0798942fb93e5123574ce01c9436e1854a518")

    def install(self, spec, prefix):
        make("prefix={0}".format(self.prefix), "install")
