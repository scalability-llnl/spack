# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTexttable(PythonPackage):
    """Python module for creating simple ASCII tables."""

    homepage = "https://github.com/foutaise/texttable/"
    pypi = "texttable/texttable-1.6.1.tar.gz"

    license("MIT")

    version("1.6.7", sha256="290348fb67f7746931bcdfd55ac7584ecd4e5b0846ab164333f0794b121760f2")
    version("1.6.6", sha256="e106b1204b788663283784fd6e5dfc23f1574b84e518e5d286c1a1e66dabd42c")
    version("1.6.5", sha256="fc3f763a89796ae03789a02343bd4e8fed9735935123b1bfb9537a5935852315")
    version("1.6.4", sha256="42ee7b9e15f7b225747c3fa08f43c5d6c83bc899f80ff9bae9319334824076e9")
    version("1.6.3", sha256="ce0faf21aa77d806bbff22b107cc22cce68dc9438f97a2df32c93e9afa4ce436")
    version("1.6.2", sha256="eff3703781fbc7750125f50e10f001195174f13825a92a45e9403037d539b4f4")
    version("1.6.1", sha256="2b60a5304ccfbeac80ffae7350d7c2f5d7a24e9aab5036d0f82489746419d9b2")

    depends_on("py-setuptools", type="build")
