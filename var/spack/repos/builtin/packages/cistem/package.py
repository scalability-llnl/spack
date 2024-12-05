# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Cistem(AutotoolsPackage):
    """cisTEM is user-friendly software to process cryo-EM images of
    macromolecular complexes and obtain high-resolution 3D reconstructions
    from them."""

    homepage = "https://cistem.org/"
    url = "https://cistem.org/system/tdf/upload3/cistem-1.0.0-beta-source-code.tar.gz?file=1&type=cistem_details&id=37&force=0"

    license("GPL-2.0-only")

    version(
        "1.0.0-beta", sha256="c62068f53d0a269ffa1bfff34641597d3795989a930686437fba9eed7a991af6"
    )

    depends_on("wxwidgets@3.0.2")
    depends_on("fftw")
    depends_on("libtiff")
