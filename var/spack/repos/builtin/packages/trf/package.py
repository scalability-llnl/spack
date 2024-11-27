# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Trf(AutotoolsPackage):
    """Tandem Repeats Finder is a program to locate and display tandem repeats
    in DNA sequences.

    Note: A manual download is required for TRF.
    Spack will search your current directory for the download file.
    Alternatively, add this file to a mirror so that Spack can find it.
    For instructions on how to set up a mirror, see
    https://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://tandem.bu.edu/trf/trf.html"
    url = "https://github.com/Benson-Genomics-Lab/TRF/archive/refs/tags/v4.09.1.tar.gz"

    license("AGPL-3.0-only")

    version("4.09.1", sha256="516015b625473350c3d1c9b83cac86baea620c8418498ab64c0a67029c3fb28a")
    version("4.09", sha256="9332155384bef82f6c7c449c038d27f1a14b984b2e93000bfcf125f4d44d6aca")

    # Beginning with version 4.09, trf is open source and available via github.
    # Only version 4.07b needs to be installed as a binary.
    manual_download = True

    version(
        "4.07b",
        sha256="a3a760c7b74c9603fbc08d95e8fa696c00f35a2f179b0bd63b2b13757ad3b471",
        expand=False,
        url="file://{0}/trf407b.linux64".format(os.getcwd()),
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    @when("@4.07b")
    def autoreconf(self, spec, prefix):
        touch("configure")

    @when("@4.07b")
    def configure(self, spec, prefix):
        pass

    @when("@4.07b")
    def build(self, spec, prefix):
        pass

    @when("@4.07b")
    def install(self, spec, prefix):
        mkdirp(prefix.bin)

        trfname = "trf{0}.linux64".format(self.version.joined)

        install(trfname, prefix.bin)
        chmod = which("chmod")
        chmod("+x", os.path.join(prefix.bin, trfname))
        os.symlink(trfname, prefix.bin.trf)
