# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJax(PythonPackage):
    """JAX is Autograd and XLA, brought together for high-performance
    machine learning research. With its updated version of Autograd,
    JAX can automatically differentiate native Python and NumPy
    functions. It can differentiate through loops, branches,
    recursion, and closures, and it can take derivatives of
    derivatives of derivatives. It supports reverse-mode
    differentiation (a.k.a. backpropagation) via grad as well as
    forward-mode differentiation, and the two can be composed
    arbitrarily to any order."""

    homepage = "https://github.com/google/jax"
    pypi = "jax/jax-0.4.27.tar.gz"

    license("Apache-2.0")
    maintainers("adamjstewart", "jonas-eschle")

    version("0.4.31", sha256="fd2d470643a0073d822737f0788f71391656af7e62cc5b2e7995ee390ceac287")
    version("0.4.30", sha256="94d74b5b2db0d80672b61d83f1f63ebf99d2ab7398ec12b2ca0c9d1e97afe577")
    version("0.4.29", sha256="12904571eaefddcdc8c3b8d4936482b783d5a216e99ef5adcd3522fdfb4fc186")
    version("0.4.28", sha256="dcf0a44aff2e1713f0a2b369281cd5b79d8c18fc1018905c4125897cb06b37e9")
    version("0.4.27", sha256="f3d7f19bdc0a17ccdb305086099a5a90c704f904d4272a70debe06ae6552998c")
    version("0.4.26", sha256="2cce025d0a279ec630d550524749bc8efe25d2ff47240d2a7d4cfbc5090c5383")
    version("0.4.25", sha256="a8ee189c782de2b7b2ffb64a8916da380b882a617e2769aa429b71d79747b982")
    version("0.4.24", sha256="4a6b6fd026ddd22653c7fa2fac1904c3de2dbe845b61ede08af9a5cc709662ae")
    version("0.4.23", sha256="2a229a5a758d1b803891b2eaed329723f6b15b4258b14dc0ccb1498c84963685")
    version("0.4.22", sha256="801434dda6e14f82a45fff753969a33281ab22fb2a50fe801b651390321057ba")
    version("0.4.21", sha256="c97fd0d2751d6e1eb15aa2052ff7cfdc129f8fafc2c14cd779720658926a587b")
    version("0.4.20", sha256="ea96a763a8b1a9374639d1159ab4de163461d01cd022f67c34c09581b71ed2ac")
    version("0.4.19", sha256="29f87f9a50964d3ca5eeb2973de3462f0e8b4eca6d46027894a0e9a903420601")
    version("0.4.18", sha256="776cf33890100803e98f45f9af10aa727271c6993d4e766c069118733c928132")
    version("0.4.17", sha256="d7508a69e87835f534cb07a2f21d79cc1cb8c4cfdcf7fb010927267ef7355f1d")
    version("0.4.16", sha256="e2ca82c9bf973c2c1c01f5340a583692b31f277aa3abd0544229c1fe5fa44b02")
    version("0.4.15", sha256="2aa123ccef591e355dea94a6e714b6559f8e1d6368a576a223f97d031ece0d15")
    version("0.4.14", sha256="18fed3881f26e8b13c8cb46eeeea3dba9eb4d48e3714d8e8f2304dd6e237083d")
    version("0.4.13", sha256="03bfe6749dfe647f16f15f6616638adae6c4a7ca7167c75c21961ecfd3a3baaa")
    version("0.4.12", sha256="d2de9a2388ffe002f16506d3ad1cc6e34d7536b98948e49c7e05bbcfe8e57998")
    version("0.4.11", sha256="8b1cd443b698339df8d8807578ee141e5b67e36125b3945b146f600177d60d79")
    version("0.4.10", sha256="1bf0f2720f778f2937301a16a4d5cd3497f13a4d6c970c24a88918a81816a888")
    version("0.4.9", sha256="1ed135cd08f48e4baf10f6eafdb4a4cdae781f9052b5838c09c91a9f4fa75f09")
    version("0.4.8", sha256="08116481f7336db16c24812bfb5e6f9786915f4c2f6ff4028331fa69e7535202")
    version("0.4.7", sha256="5e7002d74db25f97c99b979d4ba1233b1ef26e1597e5fc468ad11d1c8a9dc4f8")
    version("0.4.6", sha256="d06ea8fba4ed315ec55110396058cb48c8edb2ab0b412f28c8a123beee9e58ab")
    version("0.4.5", sha256="1633e56d34b18ddfa7d2a216ce214fa6fa712d36552532aaa71da416aede7268")
    version("0.4.4", sha256="39b07e07343ed7c74492ee5e75db77456d3afdd038a322671f09fc748f6392cb")
    version("0.4.3", sha256="d43f08f940aa30eb339965cfb3d6bee2296537b0dc2f0c65ccae3009279529ae")

    depends_on("py-setuptools", type="build")

    with default_args(type=("build", "run")):
        # setup.py
        depends_on("python@3.10:", when="@0.4.31:")
        depends_on("python@3.9:", when="@0.4.14:")
        depends_on("py-ml-dtypes@0.2:", when="@0.4.14:")
        depends_on("py-ml-dtypes@0.1:", when="@0.4.9:")
        depends_on("py-ml-dtypes@0.0.3:", when="@0.4.7:")
        depends_on("py-numpy@1.24:", when="@0.4.31:")
        depends_on("py-numpy@1.22:", when="@0.4.14:")
        depends_on("py-numpy@1.21:", when="@0.4.7:")
        depends_on("py-numpy@1.20:", when="@0.3:")
        # https://github.com/google/jax/issues/19246
        depends_on("py-numpy@:1", when="@:0.4.25")
        depends_on("py-opt-einsum")
        depends_on("py-scipy@1.10:", when="@0.4.31:")
        depends_on("py-scipy@1.9:", when="@0.4.19:")
        depends_on("py-scipy@1.7:", when="@0.4.7:")
        depends_on("py-scipy@1.5:", when="@0.3:")

        # jax/_src/lib/__init__.py
        # https://github.com/google/jax/commit/8be057de1f50756fe7522f7e98b2f30fad56f7e4
        for v in [
            "0.4.31",
            "0.4.30",
            "0.4.29",
            "0.4.28",
            "0.4.27",
            "0.4.26",
            "0.4.25",
            "0.4.24",
            "0.4.23",
            "0.4.22",
            "0.4.21",
            "0.4.20",
            "0.4.19",
            "0.4.18",
            "0.4.17",
            "0.4.16",
            "0.4.15",
            "0.4.14",
            "0.4.13",
            "0.4.12",
            "0.4.11",
            "0.4.10",
            "0.4.9",
            "0.4.8",
            "0.4.7",
            "0.4.6",
            "0.4.5",
            "0.4.4",
            "0.4.3",
        ]:
            depends_on(f"py-jaxlib@:{v}", when=f"@{v}")

        # See _minimum_jaxlib_version in jax/version.py
        depends_on("py-jaxlib@0.4.30:", when="@0.4.31:")
        depends_on("py-jaxlib@0.4.27:", when="@0.4.28:")
        depends_on("py-jaxlib@0.4.23:", when="@0.4.27:")
        depends_on("py-jaxlib@0.4.20:", when="@0.4.25:")
        depends_on("py-jaxlib@0.4.19:", when="@0.4.21:")
        depends_on("py-jaxlib@0.4.14:", when="@0.4.15:")
        depends_on("py-jaxlib@0.4.11:", when="@0.4.12:")
        depends_on("py-jaxlib@0.4.7:", when="@0.4.8:")
        depends_on("py-jaxlib@0.4.6:", when="@0.4.7:")
        depends_on("py-jaxlib@0.4.4:", when="@0.4.5:")
        depends_on("py-jaxlib@0.4.2:", when="@0.4.3:")
        depends_on("py-jaxlib@0.4.1:", when="@0.4.2:")

        # Historical dependencies
        depends_on("py-ml-dtypes@0.4:", when="@0.4.29")
        depends_on("py-importlib-metadata@4.6:", when="@0.4.11:0.4.30 ^python@:3.9")
