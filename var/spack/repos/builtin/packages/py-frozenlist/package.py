# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyFrozenlist(PythonPackage):
    """A list-like structure which implements collections.abc.MutableSequence."""

    homepage = "https://github.com/aio-libs/frozenlist"
    pypi = "frozenlist/frozenlist-1.2.0.tar.gz"

    license("Apache-2.0")

    version("1.5.0", sha256="81d5af29e61b9c8348e876d442253723928dce6433e0e76cd925cd83f1b4b817")
    version("1.3.1", sha256="3a735e4211a04ccfa3f4833547acdf5d2f863bfeb01cfd3edaffbc251f15cec8")
    version("1.3.0", sha256="ce6f2ba0edb7b0c1d8976565298ad2deba6f8064d2bebb6ffce2ca896eb35b0b")
    version("1.2.0", sha256="68201be60ac56aff972dc18085800b6ee07973c49103a8aba669dee3d71079de")

    depends_on("c", type="build")

    # Based on PyPI wheel availability
    with default_args(type=("build", "run")):
        depends_on("python@:3.13")
        depends_on("python@:3.12", when="@:1.4.1")
        depends_on("python@:3.11", when="@:1.4.0")
        depends_on("python@:3.10", when="@:1.3.1")

    with default_args(type="build"):
        depends_on("py-expandvars", when="@1.4.1:")
        depends_on("py-setuptools@47:", when="@1.4.1:")
        depends_on("py-setuptools@46.4:", when="@1.3.1:")
        depends_on("py-setuptools")
        depends_on("py-tomli", when="@1.4.1: ^python@:3.10")
        depends_on("py-wheel@0.37:", when="@1.3:1.4.0")

        # Not documented but still needed to cythonize files
        depends_on("py-cython", when="@1.4.1:")
