# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPygments(PythonPackage):
    """Pygments is a syntax highlighting package written in Python."""

    homepage = "https://pygments.org/"
    pypi = "Pygments/pygments-2.18.0.tar.gz"
    git = "https://github.com/pygments/pygments.git"

    license("BSD-2-Clause")

    version("2.18.0", sha256="786ff802f32e91311bff3889f6e9a86e81505fe99f2735bb6d60ae0c5004f199")
    version("2.16.1", sha256="1daff0494820c69bc8941e407aa20f577374ee88364ee10a98fdbe0aece96e29")
    version("2.16.0", sha256="4f6df32f21dca07a54a0a130bda9a25d2241e9e0a206841d061c85a60cc96145")
    version("2.15.1", sha256="8ace4d3c1dd481894b2005f560ead0f9f19ee64fe983366be1a21e171d12775c")
    version("2.13.0", sha256="56a8508ae95f98e2b9bdf93a6be5ae3f7d8af858b43e02c5a2ff083726be40c1")
    version("2.12.0", sha256="5eb116118f9612ff1ee89ac96437bb6b49e8f04d8a13b514ba26f620208e26eb")
    version("2.10.0", sha256="f398865f7eb6874156579fdf36bc840a03cab64d1cde9e93d68f46a425ec52c6")
    version("2.6.1", sha256="647344a061c249a3b74e230c739f434d7ea4d8b1d5f3721bc0f3558049b38f44")
    version("2.4.2", sha256="881c4c157e45f30af185c1ffe8d549d48ac9127433f2c380c24b84572ad66297")
    version("2.3.1", sha256="5ffada19f6203563680669ee7f53b64dabbeb100eb51b61996085e99c03b284a")
    version("2.2.0", sha256="dbae1046def0efb574852fab9e90209b23f556367b5a320c0bcb871c77c3e8cc")
    version("2.1.3", sha256="88e4c8a91b2af5962bfa5ea2447ec6dd357018e86e94c7d14bd8cacbc5b55d81")
    version("2.0.1", sha256="5e039e1d40d232981ed58914b6d1ac2e453a7e83ddea22ef9f3eeadd01de45cb")
    version("2.0.2", sha256="7320919084e6dac8f4540638a46447a3bd730fca172afc17d2c03eed22cf4f51")

    depends_on("py-hatchling", when="@2.17:", type="build")
    depends_on("py-setuptools@61:", when="@2.15:2.16", type=("build", "run"))
    depends_on("py-setuptools", when="@:2.14", type=("build", "run"))

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/P/Pygments/{}-{}.tar.gz"
        name = "Pygments"
        if version >= Version("2.17"):
            name = name.lower()
        return url.format(name, version)
