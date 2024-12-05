# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import archspec

from spack.package import *


class PyItk(PythonPackage):
    """ITK is an open-source toolkit for multidimensional image analysis"""

    homepage = "https://itk.org/"

    skip_version_audit = ["platform=windows"]

    if sys.platform == "darwin":
        # version 5.1.1
        version(
            "5.1.1-cp38",
            url="https://pypi.io/packages/cp35/i/itk/itk-5.1.1-cp38-cp38-macosx_10_9_x86_64.whl",
            sha256="94b09ab9dd59ceaecc456ede2b719a44b8f0d54d92409eede372c6004395ae7b",
        )

        # version 5.1.2
        version(
            "5.1.2-cp38",
            url="https://pypi.io/packages/cp38/i/itk/itk-5.1.2-cp38-cp38-macosx_10_9_x86_64.whl",
            sha256="e8dec75b4452bd2ee65beb4901b245fc3a2a2ccc46dfa008ae0b5b757718d458",
        )
        version(
            "5.1.2-cp39",
            url="https://pypi.io/packages/cp39/i/itk/itk-5.1.2-cp39-cp39-macosx_10_9_x86_64.whl",
            sha256="e8dec75b4452bd2ee65beb4901b245fc3a2a2ccc46dfa008ae0b5b757718d458",
        )

        # version 5.3.0
        version(
            "5.3.0-cp38",
            url="https://pypi.io/packages/cp38/i/itk/itk-5.3.0-cp38-cp38-macosx_10_9_x86_64.whl",
            sha256="1fbcde6f6612b13d2934722707fd7194b1d5900a655efa191dfc130bbb94df09",
        )
        version(
            "5.3.0-cp39",
            url="https://pypi.io/packages/cp39/i/itk/itk-5.3.0-cp39-cp39-macosx_10_9_x86_64.whl",
            sha256="155581581929dfe834af6c6233a8c83e2ca2b1f52d6c7b2c81f04dc249aab1a5",
        )
        version(
            "5.3.0-cp310",
            url="https://pypi.io/packages/cp310/i/itk/itk-5.3.0-cp310-cp310-macosx_10_9_x86_64.whl",
            sha256="f92ec860173c82eb458764b4b5b771783b690c3aa3a01d15c6f3d008fc2bb493",
        )
        version(
            "5.3.0-cp311",
            url="https://pypi.io/packages/cp311/i/itk/itk-5.3.0-cp311-cp311-macosx_10_9_x86_64.whl",
            sha256="9dcfd9721ff6022e91eb98dc4004d437de2912dfd50d707d1ee72b89c334a3d4",
        )
    elif sys.platform.startswith("linux"):
        # version 5.1.1
        version(
            "5.1.1-cp38",
            url="https://pypi.io/packages/cp38/i/itk/itk-5.1.1-cp38-cp38-manylinux1_x86_64.whl",
            sha256="14cd6c3a25f0d69f45eda74b006eceeaf8e2b2fcbe7c343e49683edf97e0fb14",
        )

        # version 5.1.2
        version(
            "5.1.2-cp38",
            url="https://pypi.io/packages/cp38/i/itk/itk-5.1.2-cp38-cp38-manylinux1_x86_64.whl",
            sha256="fe9225ac353116f4000c0a3440bf151200beb4a65deec5b2e626edda5b498f16",
        )
        version(
            "5.1.2-cp39",
            url="https://pypi.io/packages/cp39/i/itk/itk-5.1.2-cp39-cp39-manylinux1_x86_64.whl",
            sha256="5781b74410b7189a825c89d370411595e5e3d5dbb480201907f751f26698df83",
        )

        # version 5.3.0
        version(
            "5.3.0-cp38",
            url="https://pypi.io/packages/cp38/i/itk/itk-5.3.0-cp38-cp38-manylinux_2_28_x86_64.whl",
            sha256="d83dc2b0f5d673226ef6eacac012d1da6dd36c6126f2b3cffc7ed62231c29bf2",
        )
        version(
            "5.3.0-cp39",
            url="https://pypi.io/packages/cp39/i/itk/itk-5.3.0-cp39-cp39-manylinux_2_28_x86_64.whl",
            sha256="bcc4449f2df35224cbc26472475d2afeb8a92886a81db950b2305f911bc2a38c",
        )
        version(
            "5.3.0-cp310",
            url="https://pypi.io/packages/cp310/i/itk/itk-5.3.0-cp310-cp310-manylinux_2_28_x86_64.whl",
            sha256="272708ee5ed5d09a519b2e98ac9c130f3146630257506ea440c83501c16f9580",
        )
        version(
            "5.3.0-cp311",
            url="https://pypi.io/packages/cp311/i/itk/itk-5.3.0-cp311-cp311-manylinux_2_28_x86_64.whl",
            sha256="ba8361a8ed1c5462e690ee893f624c0babb7a1072a15609c26790eea717e3f77",
        )

    depends_on("python@3.8.0:3.8", when="@5.1.1-cp38,5.1.2-cp38,5.3.0-cp38", type=("build", "run"))
    depends_on("python@3.9.0:3.9", when="@5.1.2-cp39,5.3.0-cp39", type=("build", "run"))
    depends_on("python@3.10.0:3.10", when="@5.3.0-cp310", type=("build", "run"))
    depends_on("python@3.11.0:3.11", when="@5.3.0-cp311", type=("build", "run"))
    depends_on("py-setuptools", type="run")

    for t in set(
        [str(x.family) for x in archspec.cpu.TARGETS.values() if str(x.family) != "x86_64"]
    ):
        conflicts("target={0}:".format(t), msg="py-itk is available for x86_64 only")
