# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from glob import glob

from spack.package import *


class PyTesorter(PythonPackage):
    """
    TEsorter is coded for LTR_retriever to classify long terminal repeat
    retrotransposons (LTR-RTs) at first. It can also be used to
    classify any other transposable elements (TEs), including
    Class I and Class II elements which are covered by the
    REXdb database.
    """

    homepage = "https://github.com/zhangrengang/TEsorter"
    url = "https://github.com/zhangrengang/TEsorter/archive/refs/tags/v1.4.6.tar.gz"

    maintainers("snehring")

    license("GPL-3.0-or-later")

    version("1.4.6", sha256="c6952c98fa78d0084742fd6c7d2d1204d36db103c3cbeb19e52093cd9d311523")

    depends_on("py-setuptools", type="build")

    depends_on("py-biopython", type=("build", "run"))
    depends_on("py-xopen", type=("build", "run"))

    depends_on("hmmer@3.3:", type=("build", "run"))
    depends_on("blast-plus", type="run")

    @run_after("install")
    def run_hmmpress(self):
        hmmpress = Executable(self.spec["hmmer"].prefix.bin.hmmpress)
        db_dir = join_path(
            self.prefix,
            "lib",
            f"python{self.spec['python'].version.dotted[:2]}",
            "site-packages",
            "TEsorter",
            "database",
        )
        with working_dir(db_dir):
            for f in glob("*.hmm"):
                hmmpress(f)
