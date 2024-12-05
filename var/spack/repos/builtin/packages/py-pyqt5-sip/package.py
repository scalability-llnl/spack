# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyqt5Sip(PythonPackage):
    """The sip module support for PyQt5."""

    homepage = "https://www.riverbankcomputing.com/software/sip/"
    pypi = "PyQt5-sip/PyQt5_sip-12.9.0.tar.gz"

    license("GPL-2.0-only")

    version("12.13.0", sha256="7f321daf84b9c9dbca61b80e1ef37bdaffc0e93312edae2cd7da25b953971d91")
    version("12.12.1", sha256="8fdc6e0148abd12d977a1d3828e7b79aae958e83c6cb5adae614916d888a6b10")
    version("12.9.0", sha256="d3e4489d7c2b0ece9d203ae66e573939f7f60d4d29e089c9f11daa17cfeaae32")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools@30.3:", type="build")

    patch(
        "https://src.fedoraproject.org/rpms/python-pyqt5-sip/raw/841f58ce66df4dfcf11713e7adb6bd301403d5a8/f/afc99fa84d0d.patch",
        sha256="82a326749b145b30eda3f0040cd7099c4c06a57a5e9626687b0a983de1ebfc3e",
        when="@12.12: %gcc@14:",
    )
