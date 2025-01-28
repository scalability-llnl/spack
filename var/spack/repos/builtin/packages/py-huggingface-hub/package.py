# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHuggingfaceHub(PythonPackage):
    """Client library to download and publish models, datasets and other repos
    on the huggingface.co hub."""

    homepage = "https://github.com/huggingface/huggingface_hub"
    pypi = "huggingface_hub/huggingface_hub-0.0.10.tar.gz"

    license("Apache-2.0")
    maintainers("adamjstewart")

    version("0.26.2", sha256="b100d853465d965733964d123939ba287da60a547087783ddff8a323f340332b")
    version("0.24.6", sha256="cc2579e761d070713eaa9c323e3debe39d5b464ae3a7261c39a9195b27bb8000")
    version("0.23.4", sha256="35d99016433900e44ae7efe1c209164a5a81dbbcd53a52f99c281dcd7ce22431")
    version("0.19.4", sha256="176a4fc355a851c17550e7619488f383189727eab209534d7cef2114dae77b22")
    version("0.14.1", sha256="9ab899af8e10922eac65e290d60ab956882ab0bf643e3d990b1394b6b47b7fbc")
    version("0.10.1", sha256="5c188d5b16bec4b78449f8681f9975ff9d321c16046cc29bcf0d7e464ff29276")
    version("0.0.10", sha256="556765e4c7edd2d2c4c733809bae1069dca20e10ff043870ec40d53e498efae2")
    version("0.0.8", sha256="be5b9a7ed36437bb10a780d500154d426798ec16803ff3406f7a61107e4ebfc2")

    variant(
        "cli",
        default=False,
        when="@0.10:",
        description="Install dependencies for CLI-specific features",
    )
    variant(
        "hf_transfer",
        default=False,
        when="@0.21:",
        description="Install hf_transfer to speed up downloads/uploads",
    )

    with default_args(type="build"):
        depends_on("py-setuptools")

    with default_args(type=("build", "run")):
        depends_on("py-filelock")
        depends_on("py-fsspec@2023.5:", when="@0.18:")
        depends_on("py-fsspec", when="@0.14:")
        depends_on("py-packaging@20.9:", when="@0.10:")
        depends_on("py-pyyaml@5.1:", when="@0.10:")
        depends_on("py-requests")
        depends_on("py-tqdm@4.42.1:", when="@0.12:")
        depends_on("py-tqdm")
        depends_on("py-typing-extensions@3.7.4.3:", when="@0.10:")
        depends_on("py-typing-extensions", when="@0.0.10:")

        with when("+cli"):
            depends_on("py-inquirerpy@0.3.4")

        with when("+hf_transfer"):
            depends_on("py-hf-transfer@0.1.4:")

    def setup_run_environment(self, env):
        if "+hf_transfer" in self.spec:
            env.set("HF_HUB_ENABLE_HF_TRANSFER", 1)
