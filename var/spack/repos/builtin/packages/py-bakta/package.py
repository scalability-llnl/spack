# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyBakta(PythonPackage):
    """Bakta: rapid & standardized annotation
    of bacterial genomes, MAGs & plasmids"""

    homepage = "https://github.com/oschwengers/bakta"
    pypi = "bakta/bakta-1.5.1.tar.gz"

    maintainers("oschwengers")

    license("GPL-3.0-only")

    version("1.9.4", sha256="10330a10e459144dc78daa26f3a73674799706e2e1653e080366b1bbb9e5a5d9")
    version("1.5.1", sha256="36781612c4eaa99e6e24a00e8ab5b27dadf21c98ae6d16432f3e78c96a4adb5d")

    variant("deepsig", default=True, description="builds with deepsig to predict signal peptides")

    depends_on("python@3.8:3.10", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-biopython@1.78:", type=("build", "run"))
    depends_on("py-xopen@1.5.0:", when="@1.8.2:", type=("build", "run"))
    depends_on("py-xopen@1.1.0:", when="@:1.8.1", type=("build", "run"))
    depends_on("py-requests@2.25.1:", type=("build", "run"))
    depends_on("py-alive-progress@3.0.1:", when="@1.7.0:", type=("build", "run"))
    depends_on("py-alive-progress@1.6.2", when="@:1.6.1", type=("build", "run"))
    depends_on("py-pyyaml@6.0:", when="@1.6.0:", type=("build", "run"))
    depends_on("trnascan-se@2.0.11:", when="@1.6.0:", type=("build", "run"))
    depends_on("trnascan-se@2.0.8:", when="@:1.5.1", type=("build", "run"))
    depends_on("aragorn@1.2.41:", when="@1.7.0:", type=("build", "run"))
    depends_on("aragorn@1.2.38:", when="@:1.6.1", type=("build", "run"))
    depends_on("infernal@1.1.4:", type=("build", "run"))
    depends_on("pilercr@1.06:", type=("build", "run"))
    depends_on("py-pyrodigal@3.1.0:", when="@1.9.0:", type=("build", "run"))
    depends_on("py-pyrodigal@2.1.0:", when="@1.7.0:1.8.2", type=("build", "run"))
    depends_on("py-pyrodigal@2.0.2:", when="@1.6.0:1.6.1", type=("build", "run"))
    depends_on("prodigal@2.6.3:", when="@:1.5.1", type=("build", "run"))
    depends_on("hmmer@3.3.2:", when="@:1.8.1", type=("build", "run"))
    depends_on("py-pyhmmer@0.10.4:", when="@1.9.4:", type=("build", "run"))
    depends_on("py-pyhmmer@0.10.0:", when="@1.8.2:1.9.3", type=("build", "run"))
    # known bug with diamond v2.1.9
    # see https://github.com/oschwengers/bakta/issues/290
    depends_on("diamond@2.1.8,2.1.10:", when="@1.9.0:", type=("build", "run"))
    depends_on("diamond@2.0.14:", when="@:1.8.2", type=("build", "run"))
    depends_on("blast-plus@2.14.0:", when="@1.9.0:", type=("build", "run"))
    depends_on("blast-plus@2.12.0:", when="@:1.8.2", type=("build", "run"))
    depends_on("amrfinder@3.11.26:", when="@1.9.0:", type=("build", "run"))
    depends_on("amrfinder@3.10.23:", when="@1.5.1", type=("build", "run"))
    depends_on("circos@0.69.8:", when="@1.6.0:", type=("build", "run"))
    depends_on("py-deepsig-biocomp@1.2.5:", when="+deepsig", type=("build", "run"))

    conflicts("platform=darwin", when="+deepsig")
