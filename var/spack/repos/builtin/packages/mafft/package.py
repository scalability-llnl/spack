# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mafft(Package):
    """MAFFT is a multiple sequence alignment program for unix-like
    operating systems.  It offers a range of multiple alignment
    methods, L-INS-i (accurate; for alignment of <~200 sequences),
    FFT-NS-2 (fast; for alignment of <~30,000 sequences), etc."""

    homepage = "https://mafft.cbrc.jp/alignment/software/index.html"
    url = "https://mafft.cbrc.jp/alignment/software/mafft-7.221-with-extensions-src.tgz"

    version("7.525", sha256="2876f4adc1a2de4ed206bc40896763bf208bf1a02bda52f8bfdd91cf52d73e4a")
    version("7.505", sha256="f54a78670fcd9960233bcc3b3dd359f395a71c0ced45a7be1cfeae19950ce6ff")
    version("7.481", sha256="7397f1193048587a3d887e46a353418e67849f71729764e8195b218e3453dfa2")
    version("7.475", sha256="bb6973ae089ea18cfbd3861a5b9d2c8b7e1543a1fdc78ac2d7cd8dbe3443f319")
    version("7.453", sha256="8b2f0d6249c575f80cd51278ab45dd149b8ac9b159adac20fd1ddc7a6722af11")
    version("7.407", sha256="1840b51a0b93f40b4d6076af996ee46396428d8dbaf7ba1d847abff9cb1463e5")
    version("7.221", sha256="0bc78111966d9b00ddfa14fa217fa5bb0c593a558674a13f02dca7bcd51f7fcf")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def install(self, spec, prefix):
        with working_dir("core"):
            make("PREFIX=%s" % prefix)
            make("PREFIX=%s" % prefix, "install")
        with working_dir("extensions"):
            make("PREFIX=%s" % prefix)
            make("PREFIX=%s" % prefix, "install")
