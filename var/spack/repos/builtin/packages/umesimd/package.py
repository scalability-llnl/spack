# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Umesimd(CMakePackage):
    """UME::SIMD is an explicit vectorization library. The library defines
    homogeneous interface for accessing functionality of SIMD registers of
    AVX, AVX2, AVX512 and IMCI (KNCNI, k1om) instruction set."""

    homepage = "https://github.com/edanor/umesimd"
    url = "https://github.com/edanor/umesimd/archive/v0.8.1.tar.gz"

    version("0.8.1", sha256="78f457634ee593495083cf8eb6ec1cf7f274db5ff7210c37b3a954f1a712d357")
    version("0.7.1", sha256="c5377f8223fbf93ad79412e4b40fd14e88a86e08aa573f49df38a159d451023d")
    version("0.6.1", sha256="15d9fde1a5c89f3c77c42550c2b55d25a581971002157a338e01104079cdf843")
    version("0.5.2", sha256="8a02c0322b38f1e1757675bb781e190b2458fb8bc508a6bd03356da248362daf")
    version("0.5.1", sha256="6b7bc62548170e15e98d9e4c57c2980d2cd46593167d6d4b83765aa57175e5ad")
    version("0.4.2", sha256="a5dd2ec7ecf781af01f7e3336975870f34bfc8c79ef4bba90ec90e43b5f5969f")
    version("0.4.1", sha256="e05b9f886164826005c8db5d2240f22cb88593c05b4fe45c81aba4d1d57a9bfa")
    version("0.3.2", sha256="90399fa64489ca4d492a57a49582f5b827d4710a691f533822fd61edc346e8f6")
    version("0.3.1", sha256="9bab8b4c70e11dbdd864a09053225c74cfabb801739e09a314ddeb1d84a43f0a")

    depends_on("cxx", type="build")  # generated
