# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Scalpel(MakefilePackage, SourceforgePackage):
    """Scalpel is a software package for detecting INDELs (INsertions and
    DELetions) mutations in a reference genome which has been sequenced
    with next-generation sequencing technology.
    """

    homepage = "https://scalpel.sourceforge.net/index.html"
    sourceforge_mirror_path = "scalpel/scalpel-0.5.4.tar.gz"

    license("MIT")

    version("0.5.4", sha256="506f731b3886def158c15fd8b74fa98390f304a507d2040972e6b09ddefac8f0")
    version("0.5.3", sha256="d45b569fe3aa5934883bc7216c243d53168351c23e020d96a46fa77a1563b65e")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("perl@5.10.0:")

    # bamtools needs to build before the others.
    parallel = False

    @run_before("install")
    def filter_sbang(self):
        """Run before install so that the standard Spack sbang install hook
        can fix up the path to the perl|python binary.
        """

        with working_dir(self.stage.source_path):
            kwargs = {"ignore_absent": True, "backup": False, "string": False}

            match = "^#!/usr/bin/env perl"
            perl = self.spec["perl"].command
            substitute = "#!{perl}".format(perl=perl)
            files = [
                "FindDenovos.pl",
                "scalpel-export",
                "scalpel-discovery",
                "FindVariants.pl",
                "FindSomatic.pl",
            ]
            filter_file(match, substitute, *files, **kwargs)

    # Scalpel doesn't actually *have* an install step.  The authors
    # expect you to unpack the tarball, build it in the resulting
    # directory, and add that directory to your PATH.  The Perl
    # scripts use `FindBin` to discover the directory in which they
    # live and they run their own dedicated copies of {bam,sam}tools
    # and etc... by explicitly naming the executables in their directory.
    #
    # Rather than trying to fix their code I just copied the juicy
    # bits into prefix.bin. It's not normal, but....
    #
    def install(self, spec, prefix):
        destdir = prefix.bin  # see the note above....

        mkdirp(destdir)

        files = [
            "FindSomatic.pl",
            "HashesIO.pm",
            "MLDBM.pm",
            "scalpel-export",
            "Utils.pm",
            "FindDenovos.pl",
            "FindVariants.pl",
            "scalpel-discovery",
            "SequenceIO.pm",
            "Usage.pm",
        ]
        for f in files:
            install(f, destdir)

        dirs = ["Text", "MLDBM", "Parallel"]
        for d in dirs:
            install_tree(d, join_path(destdir, d))

        install_tree("bamtools-2.3.0/bin", join_path(destdir, "bamtools-2.3.0", "bin"))
        install_tree("bamtools-2.3.0/lib", join_path(destdir, "bamtools-2.3.0", "lib"))

        mkdirp(join_path(destdir, "bcftools-1.1"))
        install("bcftools-1.1/bcftools", join_path(destdir, "bcftools-1.1"))

        mkdirp(join_path(destdir, "Microassembler"))
        install("Microassembler/Microassembler", join_path(destdir, "Microassembler"))

        mkdirp(join_path(destdir, "samtools-1.1"))
        install("samtools-1.1/samtools", join_path(destdir, "samtools-1.1"))
