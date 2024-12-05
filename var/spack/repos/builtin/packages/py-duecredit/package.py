# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDuecredit(PythonPackage):
    """Publications (and donations) tracer."""

    homepage = "https://github.com/duecredit/duecredit"
    pypi = "duecredit/duecredit-0.9.1.tar.gz"

    license("BSD-2-Clause-FreeBSD")

    version("0.9.2", sha256="0e0fd87e9e46ce6c94308e9f780c203fe836d89628404f8bf5af96a7457bed1c")
    version("0.9.1", sha256="f6192ce9315b35f6a67174761291e61d0831e496e8ff4acbc061731e7604faf8")
    version("0.6.5", sha256="da3746c24f048e1b2e9bd15c001f0f453a29780ebb9d26367f478a63d15dee9b")

    depends_on("py-setuptools", type="build")

    depends_on("py-requests", type=("build", "run"))
    depends_on("py-citeproc-py@0.4:", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-importlib-metadata", when="@0.9: ^python@:3.7", type=("build", "run"))
