# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLightning(PythonPackage):
    """The deep learning framework to pretrain, finetune and deploy AI models."""

    homepage = "https://github.com/Lightning-AI/pytorch-lightning"
    pypi = "lightning/lightning-2.0.0.tar.gz"
    skip_modules = ["lightning.app", "lightning.data", "lightning.store"]

    maintainers("adamjstewart")

    license("Apache-2.0")

    version("2.4.0", sha256="9156604cc56e4b2b603f34fa7f0fe5107375c8e6d85e74544b319a15faa9ed0e")
    version("2.3.3", sha256="7f454711895c1c6e455766f01fa39522e25e5ab54c15c5e5fbad342fa92bc93c")
    version("2.3.2", sha256="6d02862e7e8c9e6903c06314296d0950e677f7e67ad615c3262fe7c73d95f4b8")
    version("2.3.1", sha256="29cf87270a1779984d3614f7f748af57e3695396a25e814119840894505c334c")
    version("2.3.0", sha256="4bb4d6e3650d2d5f544ad60853a22efc4e164aa71b9596d13f0454b29df05130")
    version("2.2.5", sha256="a6c31a2052fc30fee34aec7e31ea2a117a005d049c3593fc9cfb867a34f962bf")
    version("2.2.4", sha256="4cc3fb3edf04fcd63c0ecf75087d2fa06163759fc8c1fc500b16404ac1854f77")
    version("2.2.3", sha256="9f208d57ad9c1ae40918136dbef673f02d8e9ab519d33237a6e74984bcd73d96")
    version("2.2.2", sha256="799e933bf51f3f10516b3f1acf3650e4bc063682eb5b5dc9dcbd1ebd38e03e3a")
    version("2.2.1", sha256="b3e46d596b32cafd1fb9b21fdba1b1767df97b1af5cc702693d1c51df60b19aa")
    version("2.2.0", sha256="acf47bebc924f443f90a860b84a3f5566933a930adde42e3021abb5cf466c45f")
    version("2.1.4", sha256="0e45098c700fa28c604a11ae233ce181b44aeffce2404debebc2616118431d9f")
    version("2.1.3", sha256="70867a59e6b67e7720958ceb14476a2a00f34c12ad03680faed3163ed70138e2")
    version("2.1.2", sha256="3b2599a8a719916cb03526e6570356809729680c6cda09391232e2aba0a4ed4b")
    version("2.1.1", sha256="865491940d20a9754eac7494aa18cab893e0c2b31e83743349eeeaf31dfb52db")
    version("2.1.0", sha256="1f78f5995ae7dcffa1edf34320db136902b73a0d1b304404c48ec8be165b3a93")
    version("2.0.9", sha256="2395ece6e29e12064718ff16b8edec5685df7f7095d4fee78edb0a654f5cd7eb")
    version("2.0.8", sha256="db914e211b5c3b079a821be6e4344e72d0a729163676a65c4e00aae98390ae7b")
    version("2.0.7", sha256="f05acd4ba846505d40125b4f9f0bda0804b2b0356e2ad2fd4e4bf7d1c61c8cc6")
    version("2.0.6", sha256="bff959f65eed2f626dd65e7b2cfd0d3ddcd0c4ca19ffc8f5f49a4ba4494ca528")
    version("2.0.5", sha256="77df233129b29c11df7b5e071e24e29420d5efbdbbac9cb6fb4602b7b5afce8a")
    version("2.0.4", sha256="f5f5ed75a657caa8931051590ed000d46bf1b8311ae89bb17a961c3f299dbf33")
    version("2.0.3", sha256="5a70f05e40f1d7882f81eace0d4a86fe2604b423f8df42beaabd187bfdb420cf")
    version("2.0.2", sha256="fa32d671850a5be2d961c6705c927f6f48d1cf9696f61f7d865244142e684430")
    version("2.0.1", sha256="abf4f9e10b0d97348336038db79f4efc75daa2f3f81876822273023294d6ef3e")
    version("2.0.0", sha256="dfe158aa91ac139d8bdfccc7cdb627072e0052076ae9c0459c8fa12a028dbe6c")
    version(
        "1.9.5",
        sha256="4a6ee1bf338f7677f04d339b84dd0c9c0fa407c3dacea366a111dc86476d4dec",
        deprecated=True,
    )

    depends_on("py-setuptools", type="build")

    with default_args(type=("build", "run")):
        # src/lightning/__setup__.py
        depends_on("python@3.9:", when="@2.4:")
        depends_on("python@3.8:", when="@2:")

        # src/lightning.egg-info/requires.txt
        depends_on("py-pyyaml@5.4:7")
        depends_on("py-fsspec@2022.5:2025+http", when="@2.3:")
        depends_on("py-fsspec@2022.5:2024+http", when="@2.1.3:2.2")
        depends_on("py-fsspec@2021.6.1:2024+http", when="@2.1.0:2.1.2")
        depends_on("py-fsspec@2022.5:2024+http", when="@2.0.5:2.0")
        depends_on("py-fsspec@2022.5:2023+http", when="@:2.0.4")
        depends_on("py-lightning-utilities@0.10:1", when="@2.4:")
        depends_on("py-lightning-utilities@0.8:1", when="@2.1:2.3")
        depends_on("py-lightning-utilities@0.7:1", when="@2.0")
        depends_on("py-lightning-utilities@0.6.0.post0:1", when="@:1")
        depends_on("py-packaging@20:24", when="@2.1:")
        depends_on("py-packaging@17.1:24", when="@:2.0")
        depends_on("py-torch@2.1:3", when="@2.4:")
        depends_on("py-torch@2:3", when="@2.3")
        depends_on("py-torch@1.13:3", when="@2.2:")
        depends_on("py-torch@1.12:3", when="@2.1")
        depends_on("py-torch@1.11:3", when="@2.0")
        depends_on("py-torch@1.10:3", when="@:1")
        depends_on("py-torchmetrics@0.7:2", when="@2.0.9:")
        depends_on("py-torchmetrics@0.7:1", when="@:2.0.8")
        depends_on("py-tqdm@4.57:5")
        depends_on("py-typing-extensions@4.4:5", when="@2.2:")
        depends_on("py-typing-extensions@4:5")

        # Only an alias, not actually used by the library
        # depends_on("py-pytorch-lightning", when="@2:")

        # Historical requirements
        # https://github.com/Lightning-AI/pytorch-lightning/pull/20081
        depends_on("py-setuptools", when="@:2.3")
        depends_on("py-numpy@1.17.2:2", when="@:2.3")

        with when("@:2.0"):
            depends_on("py-jinja2@:4")
            depends_on("py-arrow@1.2:2")
            depends_on("py-backoff@2.2.1:3", when="@2.0.5:")
            depends_on("py-beautifulsoup4@4.8:5")
            depends_on("py-click@:9")
            depends_on("py-croniter@1.3:1.4", when="@2.0.5:")
            depends_on("py-croniter@1.3", when="@:2.0.4")
            depends_on("py-dateutils@:1")
            depends_on("py-deepdiff@5.7:7")
            depends_on("py-fastapi@0.92:1", when="@2.0.4:")
            depends_on("py-fastapi@0.69:0.88", when="@2.0.3")
            depends_on("py-fastapi@:0.88", when="@:2.0.2")
            depends_on("py-inquirer@2.10:4")
            depends_on("py-lightning-cloud@0.5.38:", when="@2.0.9:")
            depends_on("py-lightning-cloud@0.5.37:", when="@2.0.5:")
            depends_on("py-lightning-cloud@0.5.34:", when="@2.0.3:")
            depends_on("py-lightning-cloud@0.5.31:", when="@2:")
            depends_on("py-lightning-cloud@0.5.27:", when="@:1")
            depends_on("py-psutil@:6")
            depends_on("py-pydantic@1.7.4:2.1", when="@2.0.7:")
            depends_on("py-pydantic@1.7.4:2.0", when="@2.0.6")
            depends_on("py-pydantic@1.7.4:1", when="@2.0.5")
            depends_on("py-pydantic@1.7.4:3", when="@2.0.3:2.0.4")
            depends_on("py-pydantic@:2", when="@:2.0.2")
            depends_on("py-python-multipart@0.0.5:1")
            depends_on("py-requests@:3")
            depends_on("py-rich@12.3:14", when="@2:")
            depends_on("py-rich@:14", when="@:1")
            depends_on("py-starlette", when="@2.0.3:")
            depends_on("py-starlette@:1", when="@:2.0.2")
            depends_on("py-starsessions@1.2.1:1")
            depends_on("py-traitlets@5.3:6")
            depends_on("py-urllib3@:3", when="@2.0.4:")
            depends_on("py-urllib3@:2", when="@:2.0.3")
            depends_on("py-uvicorn@:1")
            depends_on("py-websocket-client@:2")
            depends_on("py-websockets@:12", when="@2.0.5:")
            depends_on("py-websockets@:11", when="@:2.0.4")

    # https://github.com/Lightning-AI/lightning/issues/18858
    conflicts("^py-torch~distributed", when="@2.1.0")
