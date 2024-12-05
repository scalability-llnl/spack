# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Bowtie2(MakefilePackage):
    """Bowtie 2 is an ultrafast and memory-efficient tool for aligning
    sequencing reads to long reference sequences"""

    homepage = "https://bowtie-bio.sourceforge.net/bowtie2/index.shtml"
    url = "https://downloads.sourceforge.net/project/bowtie-bio/bowtie2/2.3.1/bowtie2-2.3.1-source.zip"

    license("GPL-3.0-or-later")

    version("2.5.2", sha256="2c47a7da0a507c68319b307cdd15dee385127cc817d6bbf1d357af8d8af578ef")
    version("2.5.1", sha256="cb6cbbbb5a7167a2f21a3d63cb9774336361f540e1ec3d8ff907f955c35f71b8")
    version("2.4.5", sha256="d3cbd5f323393b5649aea10325d7c4b77f02035a8b204e5ac18eba95236e076a")
    version("2.4.2", sha256="4cc555eeeeb8ae2d47aaa1551f3f01b57f567a013e4e0d1f30e90f462865027e")
    version("2.4.1", sha256="566d6fb01a361883747103d797308ee4bdb70f6db7d27bfc72a520587815df22")
    version("2.3.5.1", sha256="335c8dafb1487a4a9228ef922fbce4fffba3ce8bc211e2d7085aac092155a53f")
    version("2.3.5", sha256="2b6b2c46fbb5565ba6206b47d07ece8754b295714522149d92acebefef08347b")
    version("2.3.4.1", sha256="a1efef603b91ecc11cfdb822087ae00ecf2dd922e03c85eea1ed7f8230c119dc")
    version("2.3.1", sha256="33bd54f5041a31878e7e450cdcf0afba08345fa1133ce8ac6fd00bf7e521a443")
    version("2.3.0", sha256="f9f841e780e78b1ae24b17981e2469e6d5add90ec22ef563af23ae2dd5ca003c")
    version("2.2.5", sha256="e22766dd9421c10e82a3e207ee1f0eb924c025b909ad5fffa36633cd7978d3b0")

    depends_on("tbb", when="@2.3.0:")
    depends_on("readline", when="@2.3.1:")
    depends_on("perl", type="run")
    depends_on("python", type="run")
    depends_on("zlib-api", when="@2.3.1:")
    depends_on("simde", when="@2.4.0: target=aarch64:", type="link")
    depends_on("simde", when="@2.4.0: target=ppc64le:", type="link")

    patch("bowtie2-2.2.5.patch", when="@2.2.5", level=0)
    patch("bowtie2-2.3.1.patch", when="@2.3.1", level=0)
    patch("bowtie2-2.3.0.patch", when="@2.3.0", level=0)

    # seems to have trouble with 6's -std=gnu++14
    conflicts("%gcc@6:", when="@:2.3.1")
    conflicts("^intel-oneapi-tbb", when="@:2.3.5.1")
    conflicts("@:2.3.5.0", when="target=aarch64:")
    conflicts("@2.4.1", when="target=aarch64:")

    def edit(self, spec, prefix):
        kwargs = {"ignore_absent": True, "backup": False, "string": False}

        match = "^#!/usr/bin/env perl"
        perl = spec["perl"].command
        substitute = "#!{perl}".format(perl=perl)
        files = ["bowtie2"]
        filter_file(match, substitute, *files, **kwargs)

        match = "^#!/usr/bin/env python.*"
        python = spec["python"].command
        substitute = "#!{python}".format(python=python)
        files = ["bowtie2-build", "bowtie2-inspect"]
        filter_file(match, substitute, *files, **kwargs)

        if self.spec.satisfies("@2.4.0:2.4.2 target=aarch64:") or self.spec.satisfies(
            "@2.4.0:2.4.2 target=ppc64le:"
        ):
            match = "-Ithird_party/simde"
            simdepath = spec["simde"].prefix.include
            substitute = "-I{simdepath}".format(simdepath=simdepath)
            files = ["Makefile"]
            filter_file(match, substitute, *files, **kwargs)

    @property
    def build_targets(self):
        make_arg = ["PREFIX={0}".format(self.prefix)]
        if self.spec.satisfies("target=aarch64:"):
            make_arg.append("POPCNT_CAPABILITY=0")
        return make_arg

    @property
    def install_targets(self):
        if self.spec.satisfies("@:2.3.9"):
            return ["prefix={0}".format(self.prefix), "install"]
        else:
            return ["PREFIX={0}".format(self.prefix), "install"]
