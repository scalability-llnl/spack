# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform
import sys

from spack.package import *

arch, os = platform.machine(), sys.platform


class PyWandb(PythonPackage):
    """A tool for visualizing and tracking your machine
    learning experiments."""

    homepage = "https://github.com/wandb/wandb"
    pypi = "wandb/wandb-0.13.9.tar.gz"

    maintainers("thomas-bouvier")

    license("MIT")

    if (arch == "x86_64" or arch == "x64") and os == "linux":
        version(
            "0.17.3",
            sha256="cdc18c87ed255235cddd4a89ad96624595871e24ccfe975211a375a16923759f",
            url="https://files.pythonhosted.org/packages/14/1c/faf90318ff4bcb23d533b32ca3a9db6616532f312563f46d02a0c121ecff/wandb-0.17.3-py3-none-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
            expand=False,
        )
    elif arch == "aarch64" and os == "linux":
        version(
            "0.17.3",
            sha256="7b69eb8148dca4f04d1e9c11f7d651e374f429b8ed729562e3184ce989f376f2",
            url="https://files.pythonhosted.org/packages/ac/86/470ea9af2337d3cc987939980180532afd6757107044ed6970363ef42bb7/wandb-0.17.3-py3-none-manylinux_2_17_aarch64.manylinux2014_aarch64.whl",
            expand=False,
        )
    version("0.13.9", sha256="0a17365ce1f18306ce7a7f16b943094fac7284bb85f4e52c0685705602f9e307")

    depends_on("py-setuptools", type=("build", "run"))

    depends_on("py-pathtools", type=("build", "run"))
    depends_on("py-setproctitle", type=("build", "run"))
    depends_on("py-appdirs@1.4.3:", type=("build", "run"))
    depends_on("py-protobuf@3.19:4", type=("build", "run"))
    conflicts("^py-protobuf@4.21.0")
    depends_on("py-typing-extensions", type=("build", "run"), when="^python@:3.9")

    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-click@7:", type=("build", "run"))
    conflicts("^py-click@8.0.0")
    depends_on("py-gitpython@1:", type=("build", "run"))
    depends_on("py-requests@2", type=("build", "run"))
    depends_on("py-psutil@5:", type=("build", "run"))
    depends_on("py-sentry-sdk@1.0.0:", type=("build", "run"))
    depends_on("py-dockerpy-creds@0.4.0:", type=("build", "run"))
