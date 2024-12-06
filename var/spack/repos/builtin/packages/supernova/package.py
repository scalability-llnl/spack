# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Supernova(Package):
    """Supernova is a software package for de novo assembly from Chromium
    Linked-Reads that are made from a single whole-genome library from an
    individual DNA source.

    A key feature of Supernova is that it creates diploid assemblies, thus
    separately representing maternal and paternal chromosomes over very long
    distances. Almost all other methods instead merge homologous chromosomes
    into single incorrect 'consensus' sequences. Supernova is the only
    practical method for creating diploid assemblies of large genomes.

    To install this package, you will need to go to the supernova download
    page of supernova, register with your email address and download
    supernova yourself. Spack will search your current directory for the
    download file. Alternatively, add this file yo a mirror so that Spack
    can find it. For instructions on how to set up a mirror, see
    https://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://support.10xgenomics.com/de-novo-assembly/software/overview/latest/welcome"
    manual_download = True

    version("2.1.1", sha256="2f58eb66951e257b89359134ab8e35ad638c4ed51cb3fb8121625dfcc7761938")
    version("2.0.1", md5="3697ce043c798fcb672fe0a66c56d6f0")

    depends_on("bcl2fastq2")

    def url_for_version(self, version):
        return "file://{0}/supernova-{1}.tar.gz".format(os.getcwd(), version)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix)

    def install(self, spec, prefix):
        rm = which("rm")

        # remove the broken symlinks
        if os.path.isdir("anaconda-cs/2.2.0-anaconda-cs-c7/lib"):
            rm(
                "anaconda-cs/2.2.0-anaconda-cs-c7/lib/libtcl.so",
                "anaconda-cs/2.2.0-anaconda-cs-c7/lib/libtk.so",
            )

        install_tree(".", prefix)
