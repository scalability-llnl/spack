# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFsspec(PythonPackage):
    """A specification for pythonic filesystems."""

    homepage = "https://github.com/intake/filesystem_spec"
    pypi = "fsspec/fsspec-0.4.4.tar.gz"

    license("BSD-3-Clause")

    # Requires pytest
    skip_modules = ["fsspec.tests"]

    version("2024.5.0", sha256="1d021b0b0f933e3b3029ed808eb400c08ba101ca2de4b3483fbc9ca23fcee94a")
    version("2024.3.1", sha256="f39780e282d7d117ffb42bb96992f8a90795e4d0fb0f661a70ca39fe9c43ded9")
    version("2024.2.0", sha256="b6ad1a679f760dda52b1168c859d01b7b80648ea6f7f7c7f5a8a91dc3f3ecb84")
    version("2023.10.0", sha256="330c66757591df346ad3091a53bd907e15348c2ba17d63fd54f5c39c4457d2a5")
    version("2023.1.0", sha256="fbae7f20ff801eb5f7d0bedf81f25c787c0dfac5e982d98fa3884a9cde2b5411")
    version("2022.11.0", sha256="259d5fd5c8e756ff2ea72f42e7613c32667dc2049a4ac3d84364a7ca034acb8b")
    version("2021.7.0", sha256="792ebd3b54de0b30f1ce73f0ba0a8bcc864724f2d9f248cb8d0ece47db0cbde8")
    version("2021.4.0", sha256="8b1a69884855d1a8c038574292e8b861894c3373282d9a469697a2b41d5289a6")
    version("0.9.0", sha256="3f7a62547e425b0b336a6ac2c2e6c6ac824648725bc8391af84bb510a63d1a56")
    version("0.8.0", sha256="176f3fc405471af0f1f1e14cffa3d53ab8906577973d068b976114433c010d9d")
    version("0.7.3", sha256="1b540552c93b47e83c568e87507d6e02993e6d1b30bc7285f2336c81c5014103")
    version("0.4.4", sha256="97697a46e8bf8be34461c2520d6fc4bfca0ed749b22bb2b7c21939fd450a7d63")

    variant("http", default=False, description="HTTPFileSystem support", when="@0.8.1:")

    depends_on("py-setuptools", type="build", when="@:2024.4")
    depends_on("py-hatchling", type="build", when="@2024.5:")
    depends_on("py-hatch-vcs", type="build", when="@2024.5:")
    depends_on("py-requests", type=("build", "run"), when="@:2023+http")
    depends_on("py-aiohttp", type=("build", "run"), when="+http")
