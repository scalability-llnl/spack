# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RRepr(RPackage):
    """Serializable Representations.

    String and binary representations of objects for several formats and mime
    types."""

    cran = "repr"

    license("GPL-3.0-or-later")

    version("1.1.7", sha256="73bd696b4d4211096e0d1e382d5ce6591527d2ff400cc7ae8230f0235eed021b")
    version("1.1.6", sha256="3d2e6c9b363c1ec4811688deff7fb22093cadc9e0a333930382093d93c16673f")
    version("1.1.4", sha256="6f799ca83e0940618dd8c22e62ffdce5ec11ba3366c5306ae58b55b53c097040")
    version("1.1.0", sha256="743fe018f9e3e54067a970bc38b6b8c0c0498b43f88d179ac4a959c2013a5f96")
    version("1.0.1", sha256="ecde22c17fd800e1ff5c2b2962689119aa486fba40fbc6f2c50e8d4cc61bc44b")
    version("1.0.0", sha256="98b2eb1058c1cb2caa8f98708b63726f5564b45de03d38b95ff6b963a8261f49")
    version("0.9", sha256="24cac6e98f2a7e5483cf87aaffcb37611702099b63d3783e319441b4ecd0264b")

    depends_on("r@3.0.1:", type=("build", "run"))
    depends_on("r-htmltools", type=("build", "run"), when="@0.13:")
    depends_on("r-jsonlite", type=("build", "run"), when="@0.19.1:")
    depends_on("r-pillar@1.4.0:", type=("build", "run"), when="@1.0.0:")
    depends_on("r-base64enc", type=("build", "run"), when="@0.13:")
