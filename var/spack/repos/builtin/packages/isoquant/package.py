# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Isoquant(Package):
    """IsoQuant: Transcript discovery and quantification with long RNA reads"""

    # IsoQuant is a collection of Python scripts but does not install as a
    # typical Python package, so this is a `Package` rather than a `PythonPackage`
    # and we move things into place manually ...

    homepage = "https://ablab.github.io/IsoQuant/"
    url = "https://github.com/ablab/IsoQuant/releases/download/v3.6.1/IsoQuant-3.6.1.tar.gz"

    license("GPL-2.0-only", checked_by="A-N-Other")

    version("3.6.1", sha256="6d16e47e9ca45f9a0d029940d5b84e03038d9ba3d640945e3a5087acfd7ed56d")

    depends_on("minimap2", type="run")
    depends_on("samtools", type="run")

    depends_on("python@3.8:", type="run")
    depends_on("py-gffutils@0.10.1:", type="run")
    depends_on("py-biopython@1.76:", type="run")
    depends_on("py-pandas@1.0.1:", type="run")
    depends_on("py-pybedtools@0.8.1:", type="run")
    depends_on("py-pysam@0.15:", type="run")
    depends_on("py-packaging", type="run")
    depends_on("py-pyfaidx@0.7:", type="run")
    depends_on("py-pyyaml@5.4:", type="run")
    depends_on("py-matplotlib@3.1.3:", type="run")
    depends_on("py-numpy@1.18.1:", type="run")
    depends_on("py-scipy@1.4.1:", type="run")
    depends_on("py-seaborn@0.10.0:", type="run")

    def install(self, spec, prefix):
        chmod = which("chmod")
        chmod("+x", "isoquant.py", "visualize.py")
        mkdirp(prefix.bin)
        install("*.py", prefix.bin)
        install_tree("src", prefix.bin.src)
