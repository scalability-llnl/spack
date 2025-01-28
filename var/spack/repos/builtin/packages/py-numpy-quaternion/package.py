# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNumpyQuaternion(PythonPackage):
    """This package creates a quaternion type in python, and further enables
    numpy to create and manipulate arrays of quaternions. The usual algebraic
    operations (addition and multiplication) are available, along with numerous
    properties like norm and various types of distance measures between two
    quaternions. There are also additional functions like "squad" and "slerp"
    interpolation, and conversions to and from axis-angle, matrix, and
    Euler-angle representations of rotations. The core of the code is written in
    C for speed."""

    homepage = "https://github.com/moble/quaternion"
    pypi = "numpy-quaternion/numpy_quaternion-2024.0.3.tar.gz"

    license("MIT")

    version("2024.0.3", sha256="cf39a8a4506eeda297ca07a508c10c08b3487df851a0e34f070a7bf8fab9f290")
    version(
        "2021.11.4.15.26.3",
        sha256="b0dc670b2adc8ff2fb8d6105a48769873f68d6ccbe20af6a19e899b1e8d48aaf",
        url="https://pypi.io/packages/source/n/numpy-quaternion/numpy-quaternion-2021.11.4.15.26.3.tar.gz",
    )

    depends_on("c", type="build")  # generated

    variant("scipy", default=True, description="Build with scipy support")
    variant("numba", default=True, description="Build with numba support")

    depends_on("python@3.10:", when="@2024:")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@0.61:", type="build", when="@2024:")
    depends_on("py-hatchling", type="build", when="@2024:")

    depends_on("py-numpy@1.13:", type=("build", "run"))
    depends_on("py-numpy@2", type=("build"), when="@2024:")
    depends_on("py-numpy@1.25:2", type=("run"), when="@2024:")
    depends_on("py-scipy", type=("build", "run"), when="+scipy")
    depends_on("py-scipy@1.5:1", type=("build", "run"), when="@2024:+scipy")
    depends_on("py-numba", type=("build", "run"), when="+numba")
    depends_on("py-numba@0.55:", type=("build", "run"), when="@2024:+numba")
