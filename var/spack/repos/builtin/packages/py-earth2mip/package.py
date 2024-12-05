# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEarth2mip(PythonPackage):
    """Earth-2 Model Intercomparison Project (MIP).

    A python framework that enables climate researchers and scientists to explore
    and experiment with AI models for weather and climate.
    """

    homepage = "https://github.com/NVIDIA/earth2mip"
    url = "https://github.com/NVIDIA/earth2mip/archive/refs/tags/v0.1.0.tar.gz"
    git = "https://github.com/NVIDIA/earth2mip.git"

    maintainers("adamjstewart")

    license("Apache-2.0")

    version("main", branch="main")
    version("0.1.0", sha256="a49d0607893013783d30bfcb2f80412014ab535fbcc1e96dd139b78819bd98ab")

    variant("pangu", default=False, description="Build dependencies needed for Pangu-Weather")
    variant("graphcast", default=False, description="Build dependencies needed for GraphCast")

    with default_args(type="build"):
        depends_on("py-setuptools")
        depends_on("py-setuptools-scm")

    with default_args(type=("build", "run")):
        depends_on("python@3.10:")
        depends_on("py-altair@4.2.2:")
        depends_on("py-boto3@1.26.0:", when="@main")
        depends_on("py-cdsapi@0.6.1:")
        depends_on("py-cfgrib@0.9.10.3:")
        depends_on("py-cftime")
        depends_on("py-dask@2023.1.0:")
        depends_on("py-distributed@2023.1.0:")
        depends_on("py-eccodes@1.4.0:")
        depends_on("py-ecmwflibs@0.5.2:")
        depends_on("py-ecmwf-opendata@0.2.0:", when="@main")
        depends_on("py-einops")
        depends_on("py-fsspec")
        depends_on("py-h5py@3.2.0:")
        depends_on("py-h5netcdf@1.0.0:")
        depends_on("py-importlib-metadata@6.7.0:")
        depends_on("py-joblib@1.1.0:")
        depends_on("py-loguru@0.6.0:", when="@main")
        depends_on("py-netcdf4@1.6.4:")
        depends_on("py-numpy")
        depends_on("py-nvidia-modulus@0.4.0:")
        depends_on("py-pandas@1.5.3:")
        depends_on("py-properscoring@0.1:")
        depends_on("py-pydantic@1.10:1.10.11")
        depends_on("py-pytest-timeout@2.1.0:", when="@main")
        depends_on("py-pytest-asyncio@0.21.0:")
        depends_on("py-pytest-regtest")
        depends_on("py-pytest@7.0.0:")
        depends_on("py-python-dotenv@1.0.0:")
        depends_on("py-s3fs")
        depends_on("py-setuptools@38.4:")
        depends_on("py-torch@1.13:")
        depends_on("py-torch-harmonics@0.5.0:")
        depends_on("py-tqdm@4.65.0:")
        depends_on("py-typer")
        depends_on("py-xarray")
        depends_on("py-xskillscore@0.0.24:")
        depends_on("py-zarr@2.14.2:")

    with default_args(type="run"):
        with when("+pangu"):
            depends_on("py-onnxruntime@1.15.1:")

        with when("+graphcast"):
            depends_on("py-flax@0.7.3", when="@main")
            depends_on("py-jax@0.4.16")
            depends_on("py-graphcast@0.1")
            depends_on("py-gcsfs")
            depends_on("py-gcsfs@2023.6.0:", when="@0.1.0")
