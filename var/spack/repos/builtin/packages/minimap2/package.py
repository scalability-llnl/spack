# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Minimap2(PythonPackage):
    """Minimap2 is a versatile sequence alignment program that aligns DNA or
    mRNA sequences against a large reference database.
    Mappy provides a convenient interface to minimap2."""

    homepage = "https://github.com/lh3/minimap2"
    url = "https://github.com/lh3/minimap2/releases/download/v2.2/minimap2-2.2.tar.bz2"
    git = "https://github.com/lh3/minimap2.git"

    maintainers("snehring")

    license("MIT")

    version("2.28", sha256="ffa5712735d229119f8c05722a0638ae0cc15aeb8938e29a3e52d5da5c92a0b4")
    version("2.26", sha256="6a588efbd273bff4f4808d5190957c50272833d2daeb4407ccf4c1b78143624c")
    version("2.24", sha256="9dd4c31ff082182948944bcdad6d328f64f09295d10547d72eba24189880a615")
    version("2.17", sha256="b68ac8882d33cc63e9e3246775062aeb159b6990ff7f38099172c3fe6f8a2742")
    version("2.14", sha256="9088b785bb0c33488ca3a27c8994648ce21a8be54cb117f5ecee26343facd03b")
    version("2.10", sha256="52b36f726ec00bfca4a2ffc23036d1a2b5f96f0aae5a92fd826be6680c481c20")
    version("2.2", sha256="7e8683aa74c4454a8cfe3821f405c4439082e24c152b4b834fdb56a117ecaed9")

    depends_on("c", type="build")  # generated

    conflicts("target=aarch64:", when="@:2.10")
    depends_on("zlib-api", type="link")
    depends_on("py-setuptools", type="build")
    depends_on("py-cython", type="build")

    variant("jstools", default=False, description="Include Javascript tools (paftools)")
    depends_on("k8", type="run", when="+jstools")

    @run_after("install")
    def install_minimap2(self):
        make_arg = []
        if self.spec.target.family == "aarch64":
            make_arg.extend(["arm_neon=1", "aarch64=1"])
        make(*make_arg)
        mkdirp(prefix.bin)
        install("minimap2", prefix.bin)
        install("misc/*.js", prefix.bin)
