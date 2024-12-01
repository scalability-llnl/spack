# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cub(Package):
    """CUB is a C++ header library of cooperative threadblock primitives
    and other utilities for CUDA kernel programming."""

    homepage = "https://nvlabs.github.com/cub"
    url = "https://github.com/NVIDIA/cub/archive/1.12.0.zip"
    git = "https://github.com/NVIDIA/cub.git"

    license("BSD-3-Clause")

    version("2.1.0", sha256="8ec47307f5e99379ac1cf6722cd5a24fc15b84b0f5361bebd453645a5e4bb34d")
    version("1.16.0", sha256="a9e327d46c82025d17ed3ab5a10da006bcdaef5dcbd294b332ef0a572f58445b")
    version("1.15.0", sha256="dcb75744650deb42e9123509482e0f84944c1dbd60d5cd909a416d953d3a6903")
    version("1.14.0", sha256="d83ac193b6acdb9281ca130fbe9590728c018c98f38916f903181b6f9410a829")
    version("1.13.1", sha256="e17f8edee401527be626a7bd21ad85aaf903e12de3445f23d617d465d5171f61")
    version("1.13.0", sha256="741a3f26cd5b0a90421744f7112fe1e5d98fc71f4ba08a2bee1f36ac6add1fb4")
    version("1.12.1", sha256="ecf2023ae1aa669c815cc687fdbfdf60967769f301ae4a972c1aebff9719949a")
    version("1.12.0", sha256="92f0f39235db787f4850d5c4ffdaa7d5367a2f153bdd3b4a1161a6a2fefb7bfc")
    version(
        "1.12.0-rc0", sha256="c9470cb5a23849e3143a3b2f07fe4d48ed3c8e0ec862b4d4c02ec15afb4fc331"
    )
    version("1.11.0", sha256="4c5d6a42350e010273be33f72af8c9b6253cfe55e2a0584fe7bf9f84dc338d00")
    version("1.10.0", sha256="d6be1acfa65be4e25be40f576687fed19c00896390cbc6205888c69ac2f150de")
    version("1.9.10-1", sha256="6f0e6a6b2996000cefbe9bff1716689fd71c2cd4004d23b238a9cb90c4421bdc")
    version("1.9.10", sha256="063fea7c9bf87677a5fc5889e3fcd51582b77a2b3af9fa599d846a9c98ce9407")
    version("1.9.9", sha256="162514b3cc264ac89d91898b58450190b8192e2af1142cf8ccac2d59aa160dda")
    version("1.9.8-1", sha256="f61d05367bd8fe8bfb0eafa20f7b14d27deb8b25a398c53d8a97a01a2399431b")
    version("1.9.8", sha256="694845bdca04fcc67d52c14d1fe6d9b627f41e6bfec0e0987d846a4e93a136f4")
    version("1.8.0", sha256="6bfa06ab52a650ae7ee6963143a0bbc667d6504822cbd9670369b598f18c58c3")
    version("1.7.5", sha256="8f8e0b101324a9839003ff1154c8439137cd38b2039f403a92e76d5c52cee23f")
    version("1.7.4", sha256="20a1a39fd97e5da7f40f5f2e7fd73fd2ea59f9dc4bb8a6c5f228aa543e727e31")
    version("1.7.3", sha256="b7ead9e291d34ffa8074243541c1380d63be63f88de23de8ee548db573b72ebe")
    version("1.7.2", sha256="09b478d4df8e6c62f8425d23ade9e2a52bc279a20057c7d22ce2160f3923764a")
    version("1.7.1", sha256="50b8777b83093fdfdab429a61fccdbfbbb991b3bbc08385118e5ad58e8f62e1d")
    version("1.4.1", sha256="7c3784cf59f02d4a88099d6a11e357032bac9eac2b9c78aaec947d1270e21871")

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("CUB_DIR", self.prefix.include.cub.cmake)

    def install(self, spec, prefix):
        mkdirp(prefix.include)
        install_tree("cub", join_path(prefix.include, "cub"))
