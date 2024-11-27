# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class NfSeqerakit(PythonPackage):
    """A Python wrapper for the Seqera Platform CLI (formerly Tower CLI)."""

    homepage = "https://github.com/seqeralabs/seqera-kit"
    pypi = "seqerakit/seqerakit-0.4.5.tar.gz"
    maintainers("marcodelapierre")

    license("Apache-2.0")

    version("0.4.5", sha256="792bd4fa53de4b3959929413d1ad8f39e20587971c9c5451419da1ff68cf3f49")

    depends_on("nf-tower-cli", type="run")

    depends_on("python@3.8:3", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-pyyaml@6:", type=("build", "run"))
