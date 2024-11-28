# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bowtie(MakefilePackage):
    """Bowtie is an ultrafast, memory-efficient short read aligner
    for short DNA sequences (reads) from next-gen sequencers."""

    homepage = "https://sourceforge.net/projects/bowtie-bio/"
    url = "https://github.com/BenLangmead/bowtie/archive/v1.2.0.tar.gz"

    license("Artistic-2.0")

    version("1.3.1", sha256="147d9fe9652f7c5f351bfc0eb012e06981986fb43bd6bdfe88a95c02eabc6573")
    version("1.3.0", sha256="d7c2d982a67884909f284a0ff150b56b20127cd7a1ced461c3c4c03e6a6374c5")
    version("1.2.3", sha256="86402114caeacbb3a3030509cb59f0b7e96361c7b3ee2dd50e2cd68200898823")
    # The bowtie project git tagged and GitHub released a v1.2.2,
    # discovered/fixed a bug, git tagged a v1.2.2_p1 and moved the
    # 1.2.2 release to use it rather than making a new `1.2.2_p1`
    # release.
    #
    # We point both of the Spack versions at the same tarball so they
    # build the binaries that are on the release page as v1.2.2
    version("1.2.2_p1", sha256="e1b02b2e77a0d44a3dd411209fa1f44f0c4ee304ef5cc83f098275085740d5a1")
    version(
        "1.2.2",
        sha256="e1b02b2e77a0d44a3dd411209fa1f44f0c4ee304ef5cc83f098275085740d5a1",
        url="https://github.com/BenLangmead/bowtie/archive/v1.2.2_p1.tar.gz",
    )
    version("1.2.1.1", sha256="1b38408b88f61d18d7ff28b2470a8cfeefccb3fc59fd46e4cc62e23874e52c20")
    version("1.2.1", sha256="b2a7c8c879cb08f00a82665bee43e1d4861de44a87912c54d168e44c90869728")
    version("1.2.0", sha256="dc4e7951b8eca56ce7714c47fd4e84f72badd5312ee9546c912af1963570f894")
    # Keeping the old 1.2 version around for reproducibility, it's not
    # clearly identical to 1.2.0.
    version(
        "1.2",
        sha256="b1052de4253007890f6436e6361d40148bc2a5a9dd01827bb9f34097747e65f8",
        url="https://downloads.sourceforge.net/project/bowtie-bio/bowtie/1.2.0/bowtie-1.2-source.zip",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # 1.2.2 and 1.2.2_p1 fail to build with %gcc@8.3.0
    # with and without issue-87 patch
    conflicts("%gcc@8:", when="@1.2.2")
    conflicts("%gcc@8:", when="@1.2.2_p1")

    variant("tbb", default=False, description="Use Intel thread building block")

    depends_on("tbb", when="+tbb")
    depends_on("zlib-api")

    # See: https://github.com/BenLangmead/bowtie/issues/87, a
    # different fix is in the FreeBSD ports/package tree
    # https://svnweb.freebsd.org/ports?view=revision&revision=483954
    patch("issue-87.patch", when="@:1.2.2 %gcc@8.0.0:")

    # correspond to 'aarch64' architecture
    # reference: https://github.com/BenLangmead/bowtie/pull/13
    patch("for_aarch64.patch", when="@1.2.0:1.2 target=aarch64:")

    # measures for narrowing error
    patch("fix_narrowing_err.patch", when="@1.2.1:1.2.3")
    patch("fix_narrowing_err_1.3.0.patch", when="@1.3.0:")

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter("CC = .*", "CC = " + env["CC"])
        makefile.filter("CXX = .*", "CPP = " + env["CXX"])

    def build(self, spec, prefix):
        if spec.satisfies("+tbb"):
            make()
        else:
            make("NO_TBB=1")

    def install(self, spec, prefix):
        make("prefix={0}".format(self.prefix), "install")
