# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDatasets(PythonPackage):
    """Datasets is a lightweight library providing two main
    features: one-line dataloaders for many public datasets and
    efficient data pre-processing."""

    homepage = "https://github.com/huggingface/datasets"
    pypi = "datasets/datasets-1.8.0.tar.gz"

    maintainers("thomas-bouvier")

    license("Apache-2.0")

    version("2.20.0", sha256="3c4dbcd27e0f642b9d41d20ff2efa721a5e04b32b2ca4009e0fc9139e324553f")
    version("2.8.0", sha256="a843b69593914071f921fc1086fde939f30a63415a34cdda5db3c0acdd58aff2")
    version("1.8.0", sha256="d57c32bb29e453ee7f3eb0bbca3660ab4dd2d0e4648efcfa987432624cab29d3")

    with default_args(type="build"):
        depends_on("py-setuptools")

    with default_args(type=("build", "run")):
        depends_on("python@3.6:")
        depends_on("py-numpy@1.17:")
        depends_on("py-pandas")
        depends_on("py-requests@2.19:")
        depends_on("py-xxhash")
        depends_on("py-multiprocess")
        depends_on("py-packaging")
        with when("@:1.8.0"):
            depends_on("py-dill@:0.3.6")
            depends_on("py-fsspec", when="^python@3.8:")
            depends_on("py-fsspec@:0.8.0", when="^python@:3.7")
            depends_on("py-huggingface-hub@:0.0")
            depends_on("py-importlib-metadata", when="^python@:3.7")
            depends_on("py-pyarrow@1:3+parquet")
            depends_on("py-tqdm@4.27:4.49", when="@:1.8.0")
        with when("@2.8.0:"):
            depends_on("py-aiohttp")
            depends_on("py-pyyaml@5.1:")
            depends_on("python@3.7:")
        with when("@2.8.0"):
            depends_on("py-dill@:0.3.6")
            depends_on("py-fsspec@2021.11.1:+http")
            depends_on("py-huggingface-hub@0.2:0")
            depends_on("py-pyarrow@6:+parquet")
            depends_on("py-responses@:0.18")
            depends_on("py-tqdm@4.62.1:")
        with when("@2.20.0:"):
            depends_on("py-filelock")
            depends_on("py-dill@0.3.0:0.3.8")  # temporary upper bound
            depends_on("py-fsspec@2023.1.0:2024.5.0+http")
            depends_on("py-huggingface-hub@0.21.2:")
            depends_on("py-pyarrow@15:+parquet")
            depends_on("py-requests@2.32.2:")
            depends_on("py-tqdm@4.66.3:")
            depends_on("python@3.8:")
