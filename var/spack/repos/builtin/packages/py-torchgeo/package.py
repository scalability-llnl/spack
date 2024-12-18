# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTorchgeo(PythonPackage):
    """TorchGeo: datasets, samplers, transforms, and pre-trained models for geospatial data."""

    homepage = "https://github.com/microsoft/torchgeo"
    pypi = "torchgeo/torchgeo-0.1.0.tar.gz"
    git = "https://github.com/microsoft/torchgeo.git"

    license("MIT")
    maintainers("adamjstewart", "calebrob6")

    version("main", branch="main")
    version("0.6.1", sha256="38c930917ea341d05a7a611ff74c017f29482df7455d50e287ea79dec7d0a14b")
    version("0.6.0", sha256="c5b073b3c9ac06cd68e45620bab3a78fb7637fa3563aae4f75f4781ba57aee5a")
    version("0.5.2", sha256="b23df51fe53ebe66c8d555484605a5618985f3680b70275f99ce8665e7203560")
    version("0.5.1", sha256="5f86a34d18fe36eeb9146b057b21e5356252ef8ab6a9db33feebb120a01feff8")
    version("0.5.0", sha256="2bc2f9c4a19a569790cb3396499fdec17496632b0e52b86be390a2cc7a1a7033")
    version("0.4.1", sha256="a3692436bf63df8d2f9b76d16eea5ee309dd1bd74e0fde6e64456abfdb2a5b58")
    version("0.4.0", sha256="a0812487205aa2db7bc92119d896ae4bf4f1014e6fdc0ce0f75bcb24fada6613")
    version("0.3.1", sha256="ba7a716843575d173abab383c6cc2d5fc8faf5834472f16a4abe1b932040ece5")
    version("0.3.0", sha256="3d98fd58e6678555592a596bd079ed5a8b4959996ff7718d7caa48d47815b6b0")
    version("0.2.1", sha256="218bd5aed7680244688dbf0f1398f5251ad243267eb19a6a7332668ac779a1cc")
    version("0.2.0", sha256="968c4bf68c7e487bf495f2f306d8bb0f5824eb67e24b26772a510e753e04ba4c")
    version("0.1.1", sha256="6e28132f75e9d8cb3a3a0e8b443aba3cde26c8f3140b9426139ee6e8f8058b26")
    version("0.1.0", sha256="44eb3cf10ab2ac63ff95e92fcd3807096bac3dcb9bdfe15a8edac9d440d2f323")

    variant("datasets", default=False, description="Install optional dataset dependencies")
    variant("docs", default=False, description="Install documentation dependencies")
    variant("style", default=False, description="Install style checking tools")
    variant("tests", default=False, description="Install testing tools")

    # NOTE: historically, dependencies had upper bounds based on semantic version compatibility.
    # However, these were removed to improve the maintainability and flexibility of the recipe.

    # Required dependencies
    with default_args(type="build"):
        depends_on("py-setuptools@61:", when="@0.5:")
        depends_on("py-setuptools@42:")

    with default_args(type=("build", "run")):
        depends_on("python@3.10:", when="@0.6:")
        depends_on("python@3.9:", when="@0.5:")
        depends_on("py-einops@0.3:")
        depends_on("py-fiona@1.8.21:", when="@0.6:")
        depends_on("py-fiona@1.8.19:", when="@0.5:")
        depends_on("py-fiona@1.8:", when="@0.3:")
        depends_on("py-fiona@1.5:")
        depends_on("py-kornia@0.7.3:", when="@0.6:")
        depends_on("py-kornia@0.6.9:", when="@0.5:")
        depends_on("py-kornia@0.6.5:", when="@0.4:")
        depends_on("py-kornia@0.6.4:", when="@0.3:")
        depends_on("py-kornia@0.5.11:", when="@0.2:")
        depends_on("py-kornia@0.5.4:", when="@0.1:")
        depends_on("py-lightly@1.4.5:", when="@0.6:")
        depends_on("py-lightly@1.4.4:", when="@0.5:")
        depends_on("py-lightning@2:", when="@0.5:")
        depends_on("py-lightning@1.8:", when="@0.4.1:")
        depends_on("py-matplotlib@3.5:", when="@0.6:")
        depends_on("py-matplotlib@3.3.3:", when="@0.5:")
        depends_on("py-matplotlib@3.3:")
        depends_on("py-numpy@1.21.2:", when="@0.6:")
        depends_on("py-numpy@1.19.3:", when="@0.5:")
        depends_on("py-numpy@1.17.2:")
        depends_on("py-pandas@1.3.3:", when="@0.6:")
        depends_on("py-pandas@1.1.3:", when="@0.5:")
        depends_on("pil@8.4:", when="@0.6:")
        depends_on("pil@8:", when="@0.5:")
        depends_on("pil@6.2:")
        depends_on("py-pyproj@3.3:", when="@0.6:")
        depends_on("py-pyproj@3:", when="@0.5:")
        depends_on("py-pyproj@2.2:")
        depends_on("py-rasterio@1.3:", when="@0.6:")
        depends_on("py-rasterio@1.2:", when="@0.5:")
        depends_on("py-rasterio@1.0.20:", when="@0.3:")
        depends_on("py-rasterio@1.0.16:")
        depends_on("py-rtree@1:", when="@0.3:")
        depends_on("py-rtree@0.9.4:", when="@0.2.1:")
        depends_on("py-rtree@0.5:")
        depends_on("py-segmentation-models-pytorch@0.2:")
        depends_on("py-shapely@1.8:", when="@0.6:")
        depends_on("py-shapely@1.7.1:", when="@0.5:")
        depends_on("py-shapely@1.3:")
        depends_on("py-timm@0.4.12:")
        depends_on("py-torch@1.13:", when="@0.6:")
        depends_on("py-torch@1.12:", when="@0.4:")
        depends_on("py-torch@1.9:", when="@0.2:")
        depends_on("py-torch@1.7:")
        depends_on("py-torchmetrics@0.10:", when="@0.4:")
        depends_on("py-torchmetrics@0.7:")
        depends_on("py-torchvision@0.14:", when="@0.6:")
        depends_on("py-torchvision@0.13:", when="@0.4:")
        depends_on("py-torchvision@0.10:", when="@0.2:")
        depends_on("py-torchvision@0.3:")

        # Only part of lightning[pytorch-extra] we actually require.
        depends_on("py-jsonargparse@4.26.1:+signatures", when="@0.5:")

        # Historical dependencies
        depends_on("py-omegaconf@2.1:", when="@:0.4.0")
        depends_on("py-packaging@17:", when="@0.3")
        depends_on("py-pytorch-lightning@1.5.1:", when="@0.3.1:0.4.0")
        # https://github.com/microsoft/torchgeo/pull/697
        depends_on("py-pytorch-lightning@1.5.1:1.8", when="@0.3.0")
        depends_on("py-pytorch-lightning@1.3:1.8", when="@:0.2")
        depends_on("py-scikit-learn@0.21:", when="@0.3:0.4")
        depends_on("py-scikit-learn@0.18:", when="@:0.2")

    # Optional dependencies
    with when("+datasets"), default_args(type="run"):
        depends_on("py-h5py@3.6:", when="@0.6:")
        depends_on("py-h5py@3:", when="@0.5:")
        depends_on("py-h5py@2.6:")
        depends_on("py-laspy@2:", when="@0.2:")
        depends_on("opencv@4.5.4:", when="@0.6:")
        depends_on("opencv@4.4.0.46:", when="@0.5:")
        depends_on("opencv@3.4.2.17:")
        depends_on("py-pycocotools@2.0.7:", when="@0.6:")
        depends_on("py-pycocotools@2.0.5:", when="@0.5:")
        depends_on("py-pycocotools@2:")
        depends_on("py-pyvista@0.34.2:", when="@0.5:")
        depends_on("py-pyvista@0.20:", when="@0.4:")
        depends_on("py-scikit-image@0.19:", when="@0.6:")
        depends_on("py-scikit-image@0.18:", when="@0.4:")
        depends_on("py-scipy@1.7.2:", when="@0.6:")
        depends_on("py-scipy@1.6.2:", when="@0.4:")
        depends_on("py-scipy@1.2:", when="@0.3:")
        depends_on("py-scipy@0.9:")

        # Required to download SpaceNet datasets.
        depends_on("awscli-v2", when="@0.6:")
        # Required to download Source Cooperative datasets.
        depends_on("azcopy", when="@0.6:")
        # Required to download Google Drive datasets.
        depends_on("py-gdown", when="^py-torchvision@0.17.1:")
        # bz2 required to extract .tar.bz2 files, zlib required to extract .tar.gz files.
        depends_on("python+bz2+zlib")
        # JPEG, JPEG2000, TIFF, compressed PNG support required for file I/O in several datasets.
        depends_on("py-pillow+jpeg+jpeg2000+tiff+zlib", when="^[virtuals=pil] py-pillow")
        depends_on("py-pillow-simd+jpeg+jpeg2000+tiff+zlib", when="^[virtuals=pil] py-pillow-simd")
        # GDAL and libtiff are both dependencies of rasterio.
        # Sentinel 2 dataset requires OpenJPEG to read .jp2 files.
        depends_on("gdal+openjpeg", when="@0.3.1:")
        # JPEG required for GDAL to read JPEG files
        # LIBDEFLATE, ZLIB, and ZSTD required for compressed file I/O.
        depends_on("libtiff+jpeg+libdeflate+zlib+zstd")
        # LandCover.ai dataset requires ability to read .tif and write .jpg and .png files.
        # Doing this from Python requires both imgcodecs and Python bindings.
        depends_on("opencv+imgcodecs+jpeg+png+python3+tiff")

        # Historical dependencies
        depends_on("open3d@0.11.2:+python", when="@0.2:0.3")
        # https://github.com/microsoft/torchgeo/pull/1537
        depends_on("py-pandas@0.23.2:2.0", when="@0.3:0.4")
        depends_on("py-pandas@0.19.1:2.0", when="@0.2")
        depends_on("py-radiant-mlhub@0.3:", when="@0.4.1:0.5")
        depends_on("py-radiant-mlhub@0.2.1:0.4", when="@:0.4.0")
        depends_on("py-rarfile@4:", when="@0.5")
        depends_on("py-rarfile@3:", when="@:0.4")
        depends_on("py-zipfile-deflate64@0.2:", when="@0.2.1:0.5")

    with when("+docs"), default_args(type="run"):
        depends_on("py-ipywidgets@7:")
        depends_on("py-nbsphinx@0.8.5:")
        depends_on("py-pytorch-sphinx-theme")
        depends_on("py-sphinx@4:5")

    with when("+style"), default_args(type="run"):
        depends_on("prettier@3:", when="@0.6:")
        depends_on("py-mypy@0.900:")
        depends_on("py-ruff@0.2:", when="@0.6:")

        # Historical dependencies
        depends_on("py-black@21.8:+jupyter", when="@0.3:0.5")
        depends_on("py-black@21:", when="@:0.2")
        depends_on("py-flake8@3.8:", when="@:0.5")
        depends_on("py-isort@5.8:+colors", when="@:0.5")
        depends_on("py-pydocstyle@6.1:+toml", when="@:0.5")
        depends_on("py-pyupgrade@2.8:", when="@0.5")
        depends_on("py-pyupgrade@1.24:", when="@0.3:0.4")

    with when("+tests"), default_args(type="run"):
        depends_on("py-nbmake@1.3.3:", when="@0.4.1:")
        depends_on("py-nbmake@0.1:", when="@0.3.1:")
        depends_on("py-nbmake@0.1:1.1", when="@:0.3.0")
        depends_on("py-pytest@7.3:", when="@0.6:")
        depends_on("py-pytest@6.2:", when="@0.5:")
        depends_on("py-pytest@6.1.2:")
        depends_on("py-pytest-cov@4:", when="@0.6:")
        depends_on("py-pytest-cov@2.4:")

        # Historical dependencies
        depends_on("py-omegaconf@2.1:", when="@0.4.1")
        depends_on("py-tensorboard@2.9.1:", when="@0.4.1")

    # https://github.com/microsoft/torchgeo/pull/1123
    conflicts("py-kornia@0.6.10:", when="@:0.4.0")
    # https://github.com/Lightning-AI/pytorch-lightning/issues/19977
    conflicts("py-lightning@2.3", when="@0.4.1:")
    # https://github.com/microsoft/torchgeo/pull/2151
    conflicts("py-numpy@2:", when="@:0.5")
    # https://github.com/rasterio/rasterio/issues/3196
    conflicts("py-rasterio@1.4:")
