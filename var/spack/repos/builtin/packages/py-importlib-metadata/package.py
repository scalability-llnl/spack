# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyImportlibMetadata(PythonPackage):
    """Read metadata from Python packages."""

    homepage = "https://importlib-metadata.readthedocs.io/"
    pypi = "importlib_metadata/importlib_metadata-1.2.0.tar.gz"
    git = "https://github.com/python/importlib_metadata"

    license("Apache-2.0")

    version("7.0.1", sha256="f238736bb06590ae52ac1fab06a3a9ef1d8dce2b7a35b5ab329371d6c8f5d2cc")
    version("6.6.0", sha256="92501cdf9cc66ebd3e612f1b4f0c0765dfa42f0fa38ffb319b6bd84dd675d705")
    version("5.1.0", sha256="d5059f9f1e8e41f80e9c56c2ee58811450c31984dfa625329ffd7c0dad88a73b")
    version("4.12.0", sha256="637245b8bab2b6502fcbc752cc4b7a6f6243bb02b31c5c26156ad103d3d45670")
    version("4.11.4", sha256="5d26852efe48c0a32b0509ffbc583fda1a2266545a78d104a6f4aff3db17d700")
    version("4.11.1", sha256="175f4ee440a0317f6e8d81b7f8d4869f93316170a65ad2b007d2929186c8052c")
    version("4.8.3", sha256="766abffff765960fcc18003801f7044eb6755ffae4521c8e8ce8e83b9c9b0668")
    version("4.8.2", sha256="75bdec14c397f528724c1bfd9709d660b33a4d2e77387a3358f20b848bb5e5fb")
    version("4.8.1", sha256="f284b3e11256ad1e5d03ab86bb2ccd6f5339688ff17a4d797a0fe7df326f23b1")
    version("4.6.4", sha256="7b30a78db2922d78a6f47fb30683156a14f3c6aa5cc23f77cc8967e9ab2d002f")
    version("4.6.1", sha256="079ada16b7fc30dfbb5d13399a5113110dab1aa7c2bc62f66af75f0b717c8cac")
    version("3.10.1", sha256="c9356b657de65c53744046fa8f7358afe0714a1af7d570c00c3835c2d724a7c1")
    version("3.10.0", sha256="c9db46394197244adf2f0b08ec5bc3cf16757e9590b02af1fca085c16c0d600a")
    version("2.0.0", sha256="77a540690e24b0305878c37ffd421785a6f7e53c8b5720d211b211de8d0e95da")
    version("1.7.0", sha256="90bb658cdbbf6d1735b6341ce708fc7024a3e14e99ffdc5783edea9f9b077f83")
    version("1.2.0", sha256="41e688146d000891f32b1669e8573c57e39e5060e7f5f647aa617cd9a9568278")
    version("0.23", sha256="aa18d7378b00b40847790e7c27e11673d7fed219354109d0e7b9e5b25dc3ad26")
    version("0.19", sha256="23d3d873e008a513952355379d93cbcab874c58f4f034ff657c7a87422fa64e8")
    version("0.18", sha256="cb6ee23b46173539939964df59d3d72c3e0c1b5d54b84f1d8a7e912fe43612db")

    depends_on("python@3.8:", when="@6.8.0:", type=("build", "run"))
    # lowerbound needed as spack itself supports python 3.6 (can be dropped in spack 0.21)
    depends_on("python@3.7:", when="@4.9.0:", type=("build", "run"))
    depends_on("py-setuptools@56:", when="@4.6.4:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm@3.4.1:+toml", when="@3:", type="build")
    depends_on("py-setuptools-scm", type="build")

    depends_on("py-zipp@0.5:", type=("build", "run"))
    depends_on("py-typing-extensions@3.6.4:", when="@3: ^python@:3.7", type=("build", "run"))
