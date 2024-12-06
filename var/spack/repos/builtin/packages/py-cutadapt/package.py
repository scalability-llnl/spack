# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCutadapt(PythonPackage):
    """Cutadapt finds and removes adapter sequences, primers, poly-A tails and
    other types of unwanted sequence from your high-throughput sequencing
    reads."""

    homepage = "https://cutadapt.readthedocs.io"
    pypi = "cutadapt/cutadapt-1.13.tar.gz"
    git = "https://github.com/marcelm/cutadapt.git"

    license("MIT")

    version("4.7", sha256="8738a35b363eaf615665a4e7d1b4beb385cd93fb7ffdcf82cd4ab6457acc879b")
    version("4.4", sha256="4554157c673022e1c433fcd6e3b803008fef60c8e71c01215e4aa04b0f09fe83")
    version("4.3", sha256="319de860f975977e080ea42d9d255322060693ca39b7be51187831311702fe29")
    version("4.2", sha256="ab0ac450baecc1576cc5ccbc06eab2685be9ee7676763938237d954a644237f1")
    version("4.1", sha256="be745ff24adfb4a3eaf715dfad0e2ccdfad7792ef00c1122adf4fbf3aed9227b")
    version("2.10", sha256="936b88374b5b393a954852a0fe317a85b798dd4faf5ec52cf3ef4f3c062c242a")
    version("2.9", sha256="cad8875b461ca09cea498b4f0e78b0d3dcd7ea84d27d51dac4ed45080bf1499e")
    version("2.5", sha256="ced79e49b93e922e579d0bb9d21298dcb2d7b7b1ea721feed484277e08b1660b")
    version("1.13", sha256="aa9f2c1f33dc081fe94f42b1250e4382b8fb42cabbf6e70a76ff079f211d5fc0")

    # version 4 deps
    depends_on("python@3.8:", type=("build", "run"), when="@4.7:")
    depends_on("python@3.7:", type=("build", "run"), when="@4.1:4.6")
    depends_on("py-setuptools@63:", type="build", when="@4.2:")
    depends_on("py-setuptools@43:", type="build", when="@:4.1")
    depends_on("py-setuptools-scm@6.2:+toml", type="build", when="@2.0:")
    depends_on("py-cython@0.29.20:", type="build")
    depends_on("py-dnaio@1.2.0:", type=("build", "run"), when="@4.7:")
    depends_on("py-dnaio@0.10:", type=("build", "run"), when="@4.3:4.6")
    depends_on("py-dnaio@0.9.1:", type=("build", "run"), when="@4.2")
    depends_on("py-dnaio@0.7.1:", type=("build", "run"), when="@4.1")
    depends_on("py-xopen@1.6:", type=("build", "run"), when="@4.2:")
    depends_on("py-xopen@1.1:", type=("build", "run"), when="@4.1")
    # older version deps
    depends_on("py-xopen@0.1.1:", type=("build", "run"), when="@1.13")
    depends_on("py-xopen@0.5.0:", type=("build", "run"), when="@2.0:2.3")
    depends_on("py-xopen@0.7.3:", type=("build", "run"), when="@2.4")
    depends_on("py-xopen@0.8.1:0.8", type=("build", "run"), when="@2.5")
    depends_on("py-xopen@0.8.4:0.8", type=("build", "run"), when="@2.6:2.10")
    depends_on("py-dnaio@0.3:", type=("build", "run"), when="@2.0:2.4")
    depends_on("py-dnaio@0.3", type=("build", "run"), when="@2.5")
    depends_on("py-dnaio@0.4.0:0.4", type=("build", "run"), when="@2.6")
    depends_on("py-dnaio@0.4.1:0.4", type=("build", "run"), when="@2.7:2.9")
    depends_on("py-dnaio@0.4.2:0.4", type=("build", "run"), when="@2.10")
