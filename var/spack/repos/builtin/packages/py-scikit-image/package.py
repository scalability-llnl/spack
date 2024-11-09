# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScikitImage(PythonPackage):
    """Image processing algorithms for SciPy, including IO, morphology,
    filtering, warping, color manipulation, object detection, etc."""

    homepage = "https://scikit-image.org/"
    pypi = "scikit-image/scikit_image-0.17.2.tar.gz"
    git = "https://github.com/scikit-image/scikit-image.git"

    maintainers("adamjstewart")
    license("BSD-3-Clause")

    skip_modules = [
        # Requires pytest
        "skimage.filters.rank.tests",
        # skimage.future.graph moved to skimage.graph
        "skimage.future.graph",
    ]

    version("0.24.0", sha256="5d16efe95da8edbeb363e0c4157b99becbd650a60b77f6e3af5768b66cf007ab")
    version("0.23.2", sha256="c9da4b2c3117e3e30364a3d14496ee5c72b09eb1a4ab1292b302416faa360590")
    version("0.23.1", sha256="4ff756161821568ed56523f1c4ab9094962ba79e817a9a8e818d9f51d223d669")
    version("0.23.0", sha256="f412b79c6cdf4371a7332cfc769bd62440a7e1375e8e7da171d67965d0156d48")
    version("0.22.0", sha256="018d734df1d2da2719087d15f679d19285fce97cd37695103deadfaef2873236")
    version("0.21.0", sha256="b33e823c54e6f11873ea390ee49ef832b82b9f70752c8759efd09d5a4e3d87f0")
    version("0.20.0", sha256="2cd784fce18bd31d71ade62c6221440199ead03acf7544086261ee032264cf61")
    version("0.19.3", sha256="24b5367de1762da6ee126dd8f30cc4e7efda474e0d7d70685433f0e3aa2ec450")
    version("0.18.3", sha256="ecae99f93f4c5e9b1bf34959f4dc596c41f2f6b2fc407d9d9ddf85aebd3137ca")
    version("0.18.1", sha256="fbb618ca911867bce45574c1639618cdfb5d94e207432b19bc19563d80d2f171")
    version("0.17.2", sha256="bd954c0588f0f7e81d9763dc95e06950e68247d540476e06cb77bcbcd8c2d8b3")
    version("0.14.2", sha256="1afd0b84eefd77afd1071c5c1c402553d67be2d7db8950b32d6f773f25850c1f")
    version("0.12.3", sha256="82da192f0e524701e89c5379c79200bc6dc21373f48bf7778a864c583897d7c7")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # Get dependencies for:
    #
    # @0.20:      from pyproject.toml
    # @0.18:0.19  from requirements/build.txt, requirements/default.txt, pyproject.toml
    # @0.14:0.17  from requirements/build.txt, requirements/default.txt
    # @:0.13      from requirements.txt, DEPENDS.txt

    with default_args(type=("build", "run")):
        depends_on("python@3.10:", when="@0.23")
        depends_on("python@3.9:", when="@0.22:")

    with default_args(type=("build", "link", "run")):
        depends_on("py-numpy@1.23:", when="@0.23:")
        depends_on("py-numpy@1.22:", when="@0.22:")
        depends_on("py-numpy@1.21.1:", when="@0.20:")
        depends_on("py-numpy@1.17,1.18.1:", when="@0.19")
        depends_on("py-numpy@1.16.5:1.17,1.18.1:", when="@0.18")
        depends_on("py-numpy@1.15.1:1.17,1.18.1:", when="@0.17")
        depends_on("py-numpy@1.14.1:", when="@0.16")
        depends_on("py-numpy@1.11:", when="@0.13:0.15")
        depends_on("py-numpy@1.7.2:", when="@:0.12")
        # https://github.com/scikit-image/scikit-image/issues/7282
        depends_on("py-numpy@:1", when="@:0.23.0")

    with default_args(type=("build", "run")):
        depends_on("py-scipy@1.9:", when="@0.23:")
        depends_on("py-scipy@1.8:", when="@0.20:")
        depends_on("py-scipy@1.4.1:", when="@0.19:")
        depends_on("py-scipy@1.0.1:", when="@0.17:")
        depends_on("py-scipy@0.19:", when="@0.16:")
        depends_on("py-scipy@0.17:", when="@0.13:")
        depends_on("py-scipy@0.9:")
        depends_on("py-networkx@2.8:", when="@0.20:")
        depends_on("py-networkx@2.2:", when="@0.19:")
        depends_on("py-networkx@2:", when="@0.15:")
        depends_on("py-networkx@1.8:")
        depends_on("pil@9.1:", when="@0.23:")
        depends_on("pil@9.0.1:", when="@0.20:")
        depends_on("pil@6.1:7.0,7.1.2:8.2,8.3.1:", when="@0.19:")
        depends_on("pil@4.3:7.0,7.1.2:", when="@0.17:")
        depends_on("pil@4.3:", when="@0.14:")
        depends_on("pil@2.1:")
        depends_on("py-imageio@2.33:", when="@0.23:")
        depends_on("py-imageio@2.27:", when="@0.21:")
        depends_on("py-imageio@2.4.1:", when="@0.19:")
        depends_on("py-imageio@2.3:", when="@0.16:")
        depends_on("py-imageio@2.0.1:", when="@0.15:")
        depends_on("py-tifffile@2022.8.12:", when="@0.21:")
        depends_on("py-tifffile@2019.7.26:", when="@0.17:")
        depends_on("py-packaging@21:", when="@0.21:")
        depends_on("py-packaging@20:", when="@0.19:")
        depends_on("py-lazy-loader@0.4:", when="@0.23:")
        depends_on("py-lazy-loader@0.3:", when="@0.22:")
        depends_on("py-lazy-loader@0.2:", when="@0.21:")
        depends_on("py-lazy-loader@0.1:", when="@0.20:")

    with default_args(type="build"):
        depends_on("py-meson-python@0.15:", when="@0.23:")
        depends_on("py-meson-python@0.14:", when="@0.22:")
        depends_on("py-meson-python@0.13:", when="@0.20:")
        depends_on("py-setuptools@67:", when="@0.20:")
        depends_on("py-setuptools@:59.4", when="@0.19.1:0.19")
        depends_on("py-setuptools@51:", when="@0.18:")
        depends_on("py-setuptools")
        depends_on("ninja", when="@0.20:")
        depends_on("py-cython@3.0.4:", when="@0.23:")
        depends_on("py-cython@0.29.32:", when="@0.21:")
        depends_on("py-cython@0.29.24:", when="@0.20:")
        depends_on("py-cython@0.29.24:2", when="@0.19")
        depends_on("py-cython@0.29.21:", when="@0.18")
        depends_on("py-cython@0.29.13:", when="@0.17")
        depends_on("py-cython@0.25:0.28.1,0.28.3:0.28,0.29.1:", when="@0.15:0.16")
        depends_on("py-cython@0.23.4:0.28.1,0.28.3:0.28,0.29.1:", when="@0.14.3:0.14")
        depends_on("py-cython@0.23.4:0.28.1", when="@0.14.2")
        depends_on("py-cython@0.23.4:", when="@0.14.1")
        depends_on("py-cython@0.21:", when="@0.12")
        depends_on("py-pythran", when="@0.19:")

    # dependencies for old versions
    with default_args(type="build"):
        depends_on("py-numpydoc@0.6:", when="@0.13.0:0.13")

    with default_args(type=("build", "run")):
        depends_on("py-pywavelets@1.1.1:", when="@0.17:0.21")
        depends_on("py-pywavelets@0.4:", when="@0.13:0.16")
        depends_on("py-matplotlib@2.0:2,3.0.1:", when="@0.15:0.18")
        depends_on("py-matplotlib@2:", when="@0.14:0.18")
        depends_on("py-matplotlib@1.3.1:", when="@:0.18")
        depends_on("py-six@1.10:", when="@0.14.0:0.14")
        depends_on("py-six@1.7.3:", when="@:0.14")
        depends_on("py-pooch@0.5.2:", when="@0.17.0:0.17.1")
        depends_on("py-dask+array@1:", when="@0.14.2")
        depends_on("py-dask+array@0.9:", when="@0.14.0:0.14.1")
        depends_on("py-dask+array@0.5:", when="@:0.13")
        depends_on("py-cloudpickle@0.2.1:", when="@0.14.0:0.14")

    def url_for_version(self, version):
        url = (
            "https://files.pythonhosted.org/packages/source/s/scikit-image/scikit{}image-{}.tar.gz"
        )
        if version >= Version("0.20"):
            sep = "_"
        else:
            sep = "-"
        return url.format(sep, version)
