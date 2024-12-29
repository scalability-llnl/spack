# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAttrs(PythonPackage):
    """Classes Without Boilerplate"""

    homepage = "https://attrs.org/"
    pypi = "attrs/attrs-20.3.0.tar.gz"
    git = "https://github.com/python-attrs/attrs"

    license("MIT")

    version("23.1.0", sha256="6279836d581513a26f1bf235f9acd333bc9115683f14f7e8fae46c98fc50e015")
    version("22.2.0", sha256="c9227bfc2f01993c03f68db37d1d15c9690188323c067c641f1a35ca58185f99")
    version("22.1.0", sha256="29adc2665447e5191d0e7c568fde78b21f9672d344281d0c6e1ab085429b22b6")
    version("21.4.0", sha256="626ba8234211db98e869df76230a137c4c40a12d72445c45d5f5b716f076e2fd")
    version("21.2.0", sha256="ef6aaac3ca6cd92904cdd0d83f629a15f18053ec84e6432106f7a4d04ae4f5fb")
    version("20.3.0", sha256="832aa3cde19744e49938b91fea06d69ecb9e649c93ba974535d08ad92164f700")
    version("20.2.0", sha256="26b54ddbbb9ee1d34d5d3668dd37d6cf74990ab23c828c2888dccdceee395594")
    version("20.1.0", sha256="0ef97238856430dcf9228e07f316aefc17e8939fc8507e18c6501b761ef1a42a")
    version("19.3.0", sha256="f7b7ce16570fe9965acd6d30101a28f62fb4a7f9e926b3bbc9b61f8b04247e72")
    version("19.2.0", sha256="f913492e1663d3c36f502e5e9ba6cd13cf19d7fab50aa13239e420fef95e1396")
    version("19.1.0", sha256="f0b870f674851ecbfbbbd364d6b5cbdff9dcedbc7f3f5e18a6891057f21fe399")
    version("18.1.0", sha256="e0d0eb91441a3b53dab4d9b743eafc1ac44476296a2053b6ca3af0b139faf87b")
    version("17.4.0", sha256="1c7960ccfd6a005cd9f7ba884e6316b5e430a3f1a6c37c5f87d8b43f83b54ec9")
    version("16.3.0", sha256="80203177723e36f3bbe15aa8553da6e80d47bfe53647220ccaa9ad7a5e473ccc")

    depends_on("py-hatchling", when="@23.1:", type="build")
    depends_on("py-hatch-vcs", when="@23.1:", type="build")
    depends_on("py-hatch-fancy-pypi-readme", when="@23.1:", type="build")

    with when("@:22.2.0"):
        depends_on("py-setuptools@40.6.0:", when="@19.1", type="build")
        depends_on("py-setuptools", type="build")

    depends_on("py-importlib-metadata", when="@23.1: ^python@3.7", type=("build", "run"))
