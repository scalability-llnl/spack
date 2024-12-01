# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAstroid(PythonPackage):
    """A common base representation of python source code for pylint
    and other projects."""

    homepage = "https://github.com/PyCQA/astroid"
    pypi = "astroid/astroid-2.8.3.tar.gz"

    license("LGPL-2.1-or-later")

    version("2.14.2", sha256="a3cf9f02c53dd259144a7e8f3ccd75d67c9a8c716ef183e0c1f291bc5d7bb3cf")
    version("2.12.10", sha256="81f870105d892e73bf535da77a8261aa5bde838fa4ed12bb2f435291a098c581")
    version("2.12.7", sha256="cd468be9d9d03d086d4d7e6643a59bfc025762d2c895e1e22cf21feced7bb148")
    version("2.11.6", sha256="4f933d0bf5e408b03a6feb5d23793740c27e07340605f236496cd6ce552043d6")
    version("2.11.5", sha256="f4e4ec5294c4b07ac38bab9ca5ddd3914d4bf46f9006eb5c0ae755755061044e")
    version("2.11.4", sha256="561dc6015eecce7e696ff7e3b40434bc56831afeff783f0ea853e19c4f635c06")
    version("2.8.3", sha256="0e361da0744d5011d4f5d57e64473ba9b7ab4da1e2d45d6631ebd67dd28c3cce")
    version("2.7.3", sha256="3b680ce0419b8a771aba6190139a3998d14b413852506d99aff8dc2bf65ee67c")
    version("2.5.6", sha256="8a398dfce302c13f14bab13e2b14fe385d32b73f4e4853b9bdfb64598baa1975")
    version("2.4.2", sha256="2f4078c2a41bf377eea06d71c9d2ba4eb8f6b1af2135bec27bbbb7d8f12bb703")
    version("2.3.3", sha256="71ea07f44df9568a75d0f354c49143a4575d90645e9fead6dfb52c26a85ed13a")
    version("2.2.5", sha256="6560e1e1749f68c64a4b5dee4e091fce798d2f0d84ebe638cf0e0585a343acf4")
    version("2.2.0", sha256="1d5d0e6e408701ae657342645465d08be6fb66cf0ede16a31cc6435bd2e61718")
    version("2.0.4", sha256="c7013d119ec95eb626f7a2011f0b63d0c9a095df9ad06d8507b37084eada1a8d")
    version("1.6.6", sha256="d25869fc7f44f1d9fb7d24fd7ea0639656f5355fc3089cd1f3d18c6ec6b124c7")
    version("1.4.5", sha256="729b986aa59fb77af533707c385021b04e60d136b5f21cc766618556d0816cf6")
    version("1.4.4", sha256="7f7e5512efe515098e77cbd3a60e87c8db8954097b0e025d8d6f72f2e8ddc298")
    version("1.4.3", sha256="8e9ce4e925a17442cec085a7fce05478b99e482c13819c619b7cdd793777bf6b")
    version("1.4.2", sha256="b734fa504179a93aa03314df48b45fb1d9d0d8770a1126e7a126c9ac4aebd5c3")
    version("1.4.1", sha256="2417a2c62f07bb77485efb6dd94567ac165808a4248ecb09754116662ffa9fc2")

    # fixes symlink resolution, already included in 2: but not in 1.6.6
    patch("PR546.patch", when="@1.6.6")

    # Dependencies taken from astroid/__pkginfo__.py
    depends_on("python@2.7:2.8,3.4:", when="@:1", type=("build", "run"))
    depends_on("python@3.4:", when="@2.0.0:", type=("build", "run"))
    depends_on("python@3.5:", when="@2.3.3:", type=("build", "run"))
    depends_on("python@3.6:", when="@2.5.6:", type=("build", "run"))
    depends_on("python@3.6.2:", when="@2.11.4:", type=("build", "run"))
    depends_on("python@3.7.2:", when="@2.12.7:", type=("build", "run"))
    depends_on("py-lazy-object-proxy", type=("build", "run"))
    # Starting with astroid 2.3.1, astroid's dependencies were restricted
    # to a given minor version, c.f. commit e1b4e11.
    depends_on("py-lazy-object-proxy@1.4.0:1.4", when="@2.3.1:2.7.2", type=("build", "run"))
    depends_on("py-lazy-object-proxy@1.4.0:", when="@2.7.3:", type=("build", "run"))
    depends_on("py-six", when="@:2.7.2", type=("build", "run"))
    depends_on("py-six@1.12:1", when="@2.3.3:2.7.2", type=("build", "run"))
    depends_on("py-wrapt", when="@:2.2", type=("build", "run"))
    depends_on("py-wrapt@1.11:1.12", when="@2.3.3:2.8.2", type=("build", "run"))
    depends_on("py-wrapt@1.11:1.13", when="@2.8.3:2.10", type=("build", "run"))
    depends_on("py-wrapt@1.11:1", when="@2.11", type=("build", "run"))
    depends_on("py-wrapt@1.14:1", when="@2.12.7: ^python@3.11:", type=("build", "run"))
    depends_on("py-wrapt@1.11:1", when="@2.12.7: ^python@:3.10", type=("build", "run"))
    depends_on("py-typed-ast@1.3.0:", when="@2.2.5:2.3.0 ^python@3.7.0:3.7")
    depends_on("py-typed-ast@1.4.0:1.4", when="@2.3.1:2.8.4 ^python@:3.7", type=("build", "run"))
    depends_on("py-typed-ast@1.4.0:1", when="@2.8.5: ^python@:3.7", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.4:", when="@2.7.3: ^python@:3.7", type=("build", "run"))
    depends_on("py-typing-extensions@3.10:", when="@2.8.3: ^python@:3.9", type=("build", "run"))
    depends_on("py-typing-extensions@4.0:", when="@2.14: ^python@:3.10", type=("build", "run"))
    depends_on("py-setuptools@17.1:", type=("build", "run"))
    depends_on("py-setuptools@20:", when="@2.7.3:", type=("build", "run"))
    depends_on("py-setuptools@62.6:62", when="@2.12.7:", type=("build", "run"))
    depends_on("py-wheel@0.37.1:0.37", when="@2.12.7:", type="build")
