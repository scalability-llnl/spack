# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTqdm(PythonPackage):
    """A Fast, Extensible Progress Meter"""

    homepage = "https://github.com/tqdm/tqdm"
    pypi = "tqdm/tqdm-4.45.0.tar.gz"

    version("4.66.3", sha256="23097a41eba115ba99ecae40d06444c15d1c0c698d527a01c6c8bd1c5d0647e5")
    version("4.66.1", sha256="d88e651f9db8d8551a62556d3cff9e3034274ca5d66e93197cf2490e2dcb69c7")
    version("4.65.0", sha256="1871fb68a86b8fb3b59ca4cdd3dcccbc7e6d613eeed31f4c332531977b89beb5")
    version("4.64.1", sha256="5f4f682a004951c1b450bc753c710e9280c5746ce6ffedee253ddbcbf54cf1e4")
    version("4.64.0", sha256="40be55d30e200777a307a7585aee69e4eabb46b4ec6a4b4a5f2d9f11e7d5408d")
    version("4.62.3", sha256="d359de7217506c9851b7869f3708d8ee53ed70a1b8edbba4dbcb47442592920d")
    version("4.59.0", sha256="d666ae29164da3e517fcf125e41d4fe96e5bb375cd87ff9763f6b38b5592fe33")
    version("4.58.0", sha256="c23ac707e8e8aabb825e4d91f8e17247f9cc14b0d64dd9e97be0781e9e525bba")
    version("4.56.2", sha256="11d544652edbdfc9cc41aa4c8a5c166513e279f3f2d9f1a9e1c89935b51de6ff")
    version("4.46.0", sha256="4733c4a10d0f2a4d098d801464bdaf5240c7dadd2a7fde4ee93b0a0efd9fb25e")
    version("4.45.0", sha256="00339634a22c10a7a22476ee946bbde2dbe48d042ded784e4d88e0236eca5d81")
    version("4.36.1", sha256="abc25d0ce2397d070ef07d8c7e706aede7920da163c64997585d42d3537ece3d")
    version("4.8.4", sha256="bab05f8bb6efd2702ab6c532e5e6a758a66c0d2f443e09784b73e4066e6b3a37")

    variant("telegram", default=False, description="Enable Telegram bot support")
    variant("notebook", default=False, description="Enable Jupyter Notebook support")

    depends_on("py-setuptools@42:", type=("build", "run"))
    depends_on("py-setuptools-scm@3.4:+toml", type="build")
    depends_on("py-colorama", when="platform=windows", type=("build", "run"))

    depends_on("py-requests", when="+telegram", type=("build", "run"))
    depends_on("py-ipywidgets@6:", when="+notebook", type=("build", "run"))
