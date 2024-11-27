# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyParticle(PythonPackage):
    """Particle provides a pythonic interface to the Particle Data Group (PDG)
    particle data tables and particle identification codes, with extended
    particle information and extra goodies."""

    git = "https://github.com/scikit-hep/particle.git"
    pypi = "particle/particle-0.11.0.tar.gz"
    homepage = "https://github.com/scikit-hep/particle"

    maintainers("vvolkl")

    tags = ["hep"]

    license("BSD-3-Clause")

    version("master", branch="master")
    version("0.24.0", sha256="8ab4b5dd4547ba2dae8354955a435210892a575dff46f323cac6cf40600b976a")
    version("0.23.1", sha256="eee28b0e846bfea4dfd70e9ec5ffe3244613db08b6b6a9b773f55a4310752fab")
    version("0.23.0", sha256="d810f8fc27deb8e7fd64174017d9607d50522249c0973a0008e580f93db11750")
    version("0.22.1", sha256="dcb45025cf7cff901e2c94922d150e1103245c46f2671eae4193c5fa767cc56c")
    version("0.22.0", sha256="567bb3017cb7526f9c9ef4399e9ba5acbdb5b9ce93eb18e4da6479d3181c93a5")
    version("0.21.2", sha256="0434d39aab4fc72bce452a11f822736f95937c5f4116b0e831254ebcef6cfcdb")
    version("0.21.1", sha256="330f48550a17654f01c94e8e2365ad9a8dcf26e573e8acf31fb23ea4f624b2c4")
    version("0.21.0", sha256="483748834e7e81f2cd690fa0962b537f767fe8af4705c8bada68c8bbdac8a17d")
    version("0.20.1", sha256="1e8596c2818cae446a958ceb1766a91acc6c6401f01db1d23b94c24827a5c547")
    version("0.20.0", sha256="cb3d3de2a2879c54b1c1f9077b3f6aa5cacc3a8ee1c58c8a7fe47c658f048631")
    version("0.16.3", sha256="b42fd601c7bcf0c0680db332624380c5dd6e265f0d804d054c102eae07a669ce")
    version("0.16.2", sha256="53581654ee6b3efbe0993317cff4d83f5529c1da851e12c77a6f6397956100ff")
    version("0.16.1", sha256="40413c9bae8c42d437cbb280717d9a53b34e496833efea8779eb5f5ef7bfb096")
    version("0.16.0", sha256="582371c69dd897dea3653ae82b7c2602635e4b797b832e141a856746ba9b0b98")
    version("0.15.1", sha256="6b05cdc4b76c70f785e89258a470504ad87ca119057c65da30a7d4412cca824f")
    version("0.14.1", sha256="05b345f8fbfdb12a0aa744c788b6e1b22326b5a6ad95230596e0fc9ebad56621")
    version("0.11.0", sha256="e90dc36c8b7d7431bd14ee5a28486d28b6c0708555845d1d7bdf59a165405f12")

    depends_on("python@2.7:2.8,3.5:", when="@:0.19", type=("build", "run"))
    depends_on("python@3.6:", when="@0.20:", type=("build", "run"))
    depends_on("python@3.7:", when="@0.21:", type=("build", "run"))
    depends_on("python@3.8:", when="@0.24:", type=("build", "run"))
    depends_on("py-setuptools", when="@:0.20", type="build")
    depends_on("py-setuptools-scm@3.4:+toml", when="@:0.20", type="build")
    depends_on("py-hatchling", when="@0.21:", type="build")
    depends_on("py-hatch-vcs", when="@0.21:", type="build")
    depends_on("py-importlib-resources@2:", when="@0.16: ^python@:3.8", type=("build", "run"))
    depends_on("py-typing-extensions@4.5:", when="@0.23.1: ^python@:3.12", type=("build", "run"))
    depends_on("py-typing-extensions", when="@0.16:0.23.0 ^python@:3.7", type=("build", "run"))
    depends_on("py-deprecated", when="@0.22.0:0.23.0", type=("build", "run"))

    depends_on("py-attrs@19.2.0:", type=("build", "run"))
    depends_on("py-hepunits@1.2.0:", when="@:0.12", type=("build", "run"))
    depends_on("py-hepunits@2.0.0:", when="@0.13:", type=("build", "run"))
