# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform
import sys

from spack.package import *

arch, os = platform.machine(), sys.platform
arch64_32, _ = platform.architecture()


class PyKaleido(PythonPackage):
    """Static image export for web-based visualization libraries with zero dependencies"""

    homepage = "https://github.com/plotly/Kaleido"
    pypi = "kaleido/kaleido-0.2.1-py2.py3-none-manylinux1_x86_64.whl"

    maintainers("Pandapip1")

    if (arch == "x86_64" or arch == "x64") and os == "linux":  # Linux on x86_64
        version(
            "0.2.1",
            sha256="aa21cf1bf1c78f8fa50a9f7d45e1003c387bd3d6fe0a767cfbbf344b95bdc3a8",
            url="https://files.pythonhosted.org/packages/ae/b3/a0f0f4faac229b0011d8c4a7ee6da7c2dca0b6fd08039c95920846f23ca4/kaleido-0.2.1-py2.py3-none-manylinux1_x86_64.whl",
            expand=False,
        )
    elif arch == "arm7l" and os == "linux":  # Linux on ARMv7
        version(
            "0.2.1.post1",
            sha256="d313940896c24447fc12c74f60d46ea826195fc991f58569a6e73864d53e5c20",
            url="https://files.pythonhosted.org/packages/86/4b/d668e288b694661d2fbfc2b972db69cf1f30f8b8a91be14dcf9f000cab16/kaleido-0.2.1.post1-py2.py3-none-manylinux2014_armv7l.whl",
            expand=False,
        )
    elif arch == "aarch64" and os == "linux":  # Linux on 64-bit ARM
        version(
            "0.2.1",
            sha256="845819844c8082c9469d9c17e42621fbf85c2b237ef8a86ec8a8527f98b6512a",
            url="https://files.pythonhosted.org/packages/a1/2b/680662678a57afab1685f0c431c2aba7783ce4344f06ec162074d485d469/kaleido-0.2.1-py2.py3-none-manylinux2014_aarch64.whl",
            expand=False,
        )
    elif (arch == "x86_64" or arch == "x64") and os == "darwin":  # MacOS on x86_64
        version(
            "0.2.1",
            sha256="ca6f73e7ff00aaebf2843f73f1d3bacde1930ef5041093fe76b83a15785049a7",
            url="https://files.pythonhosted.org/packages/e0/f7/0ccaa596ec341963adbb4f839774c36d5659e75a0812d946732b927d480e/kaleido-0.2.1-py2.py3-none-macosx_10_11_x86_64.whl",
            expand=False,
        )
    elif not (arch == "x86_64" or arch == "x64") and os == "darwin":  # MacOS on Apple Silicon
        version(
            "0.2.1",
            sha256="bb9a5d1f710357d5d432ee240ef6658a6d124c3e610935817b4b42da9c787c05",
            url="https://files.pythonhosted.org/packages/45/8e/4297556be5a07b713bb42dde0f748354de9a6918dee251c0e6bdcda341e7/kaleido-0.2.1-py2.py3-none-macosx_11_0_arm64.whl",
            expand=False,
        )
    elif arch64_32 == "64bit" and os == "win32":  # 64-bit windows
        version(
            "0.2.1",
            sha256="4670985f28913c2d063c5734d125ecc28e40810141bdb0a46f15b76c1d45f23c",
            url="https://files.pythonhosted.org/packages/f7/9a/0408b02a4bcb3cf8b338a2b074ac7d1b2099e2b092b42473def22f7b625f/kaleido-0.2.1-py2.py3-none-win_amd64.whl",
            expand=False,
        )
    elif arch64_32 == "32bit" and os == "win32":  # 32-bit windows
        version(
            "0.2.1",
            sha256="ecc72635860be616c6b7161807a65c0dbd9b90c6437ac96965831e2e24066552",
            url="https://files.pythonhosted.org/packages/88/89/4b6f8bb3f9ab036fd4ad1cb2d628ab5c81db32ac9aa0641d7b180073ba43/kaleido-0.2.1-py2.py3-none-win32.whl",
            expand=False,
        )

    depends_on("python", type=("build", "run"))
    depends_on("py-setuptools", type="build")
