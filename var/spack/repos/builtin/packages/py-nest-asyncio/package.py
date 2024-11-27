# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyNestAsyncio(PythonPackage):
    """Patch asyncio to allow nested event loops."""

    homepage = "https://github.com/erdewit/nest_asyncio"
    pypi = "nest-asyncio/nest_asyncio-1.4.0.tar.gz"

    license("BSD-2-Clause")

    version("1.6.0", sha256="6f172d5449aca15afd6c646851f4e31e02c598d553a667e38cafa997cfec55fe")
    version("1.5.9", sha256="d1e1144e9c6e3e6392e0fcf5211cb1c8374b5648a98f1ebe48e5336006b41907")
    version("1.5.8", sha256="25aa2ca0d2a5b5531956b9e273b45cf664cae2b145101d73b86b199978d48fdb")
    version("1.5.6", sha256="d267cc1ff794403f7df692964d1d2a3fa9418ffea2a3f6859a439ff482fef290")
    version("1.5.5", sha256="e442291cd942698be619823a17a86a5759eabe1f8613084790de189fe9e16d65")
    version("1.5.4", sha256="f969f6013a16fadb4adcf09d11a68a4f617c6049d7af7ac2c676110169a63abd")
    version("1.5.1", sha256="afc5a1c515210a23c461932765691ad39e8eba6551c055ac8d5546e69250d0aa")
    version("1.4.0", sha256="5773054bbc14579b000236f85bc01ecced7ffd045ec8ca4a9809371ec65a59c8")

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm@3.4.3: +toml", type="build")
