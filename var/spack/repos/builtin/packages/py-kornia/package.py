# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKornia(PythonPackage):
    """Open Source Differentiable Computer Vision Library for PyTorch."""

    homepage = "http://www.kornia.org/"
    pypi = "kornia/kornia-0.5.10.tar.gz"

    license("Apache-2.0")
    maintainers(
        "edgarriba",
        "ducha-aiki",
        "lferraz",
        "shijianjian",
        "cjpurackal",
        "johnnv1",
        "adamjstewart",
    )

    version("0.7.3", sha256="0eb861ea5d7e6c3891ae699a8b7103a5783af0a7c41888ca482420dd3d055306")
    version("0.7.2", sha256="f834ccd51188d071ed286a6727471c94344ea2a718903cc6f0e56a92f9c66ac5")
    version("0.7.1", sha256="65b54a50f70c1f88240b557fda3fdcc1ab866982a5d062e52213130f5a48465c")
    version("0.7.0", sha256="72cba6a0965a15caf10a664647654412effb7c0b9afcf40e458bc005f976ffac")
    version("0.6.12", sha256="e30bd3d830226f7a159dff1f7757c6200e8f27d1333f06e9d2f98bdb33ce18d3")
    version("0.6.11", sha256="ba77198f2c2e4044c87e4503ff277aadbfc0db20495da5a5289663f380b4be32")
    version("0.6.10", sha256="00b4e8990b5ccdc589e3ecc2613446623b0ffb2fe1db5598aac55513b4016903")
    version("0.6.9", sha256="b756bba0db8d47046417fa72271b2d648c570ec6f1d61e1805e6a36911f63bb9")
    version("0.6.8", sha256="0985e02453c0ab4f030e8d22a3a7554dab312ffa8f8a54ec872190e6f0b58c56")
    version("0.6.7", sha256="7ff57c931551a1a1465aaac1fa6842a2aad650f51a0f9bf6cf0b0f7d6e5fb59c")
    version("0.6.6", sha256="e29f0f994e3bafec016b101a9a3e89c3751b4fe99ada3ac21d3febb47904faa4")
    version("0.6.5", sha256="14cbd8b4064b3d0fb5a8198d1b5fd9231bcd62b9039351641fca6b294b5069f0")
    version("0.6.4", sha256="ff60307a7244b315db43bfc4d4d6769094cf7d7494cf367c1d71a56343e2c50f")
    version("0.6.3", sha256="0b689b5a47f55f2b08f61e6731760542cc3e3c09c3f0498164b934a3aef0bab3")
    version("0.6.2", sha256="eea722b3ff2f227a9ef8088cdab480cd40dd91d9138649bfd92cfa668204eea9")
    version("0.6.1", sha256="f638fb3309f88666545866c162f510b6d485fd8f7131d5570d4e6c0d295fdcd6")
    version("0.5.10", sha256="428b4b934a2ba7360cc6cba051ed8fd96c2d0f66611fdca0834e82845f14f65d")

    # pyproject.toml
    depends_on("py-setuptools@61.2:", when="@0.6.11:", type="build")
    depends_on("py-setuptools", type="build")

    # requirements/requirements.txt
    depends_on("py-kornia-rs@0.1:", when="@0.7.2:", type=("build", "run"))
    depends_on("py-packaging", when="@0.6:", type=("build", "run"))
    depends_on("py-torch@1.9.1:", when="@0.6.9:", type=("build", "run"))
    depends_on("py-torch@1.8.1:", when="@0.6:", type=("build", "run"))
    depends_on("py-torch@1.6.0:", type=("build", "run"))

    # Historical dependencies
    depends_on("py-pytest-runner", when="@:0.6.10", type="build")
