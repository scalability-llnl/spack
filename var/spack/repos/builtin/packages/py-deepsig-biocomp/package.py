# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDeepsigBiocomp(PythonPackage):
    """DeepSig - Predictor of signal peptides
    in proteins based on deep learning"""

    homepage = "https://deepsig.biocomp.unibo.it"

    url = "https://github.com/BolognaBiocomp/deepsig/archive/refs/tags/v1.2.5.tar.gz"

    license("GPL-3.0-only")

    version("1.2.5", sha256="e954b815d63c221c564c7d3fe27123d7cd2c39b191d6107369ab095d506496e0")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-biopython@1.78:", type=("build", "run"))
    depends_on("py-keras@2.4.3:", type=("build", "run"))
    depends_on("py-tensorflow@2.2.0:", type=("build", "run"))
    depends_on("py-tensorboard", type=("build", "run"))

    @run_after("install")
    def create_share_folder(self):
        share_dir = join_path(self.prefix, "share", "deepsig")
        mkdirp(share_dir)
        mv = which("mv")
        for d in ("models", "tools"):
            mv(d, share_dir)

    def setup_run_environment(self, env):
        env.set("DEEPSIG_ROOT", self.prefix.share.deepsig)
