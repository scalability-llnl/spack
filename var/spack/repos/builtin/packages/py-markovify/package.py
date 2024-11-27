# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMarkovify(PythonPackage):
    """Markovify is a simple, extensible Markov chain generator. Right
    now, its primary use is for building Markov models of large
    corpora of text and generating random sentences from that."""

    homepage = "https://github.com/jsvine/markovify"
    pypi = "markovify/markovify-0.8.3.tar.gz"

    license("MIT")

    version("0.8.3", sha256="254405c5b2f819ae388c39a53e6bc038bfbc24713441869ce90a1cd67e4a89ce")

    depends_on("py-setuptools", type="build")
    depends_on("py-unidecode", type=("build", "run"))
