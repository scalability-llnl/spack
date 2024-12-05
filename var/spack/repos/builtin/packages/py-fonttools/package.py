# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFonttools(PythonPackage):
    """fontTools is a library for manipulating fonts, written in Python.

    The project includes the TTX tool, that can convert TrueType and OpenType fonts to
    and from an XML text format, which is also called TTX. It supports TrueType,
    OpenType, AFM and to an extent Type 1 and some Mac-specific formats."""

    homepage = "https://github.com/fonttools/fonttools"
    pypi = "fonttools/fonttools-4.28.1.zip"

    skip_modules = ["fontTools.ufoLib"]

    license("MIT")

    version("4.39.4", sha256="dba8d7cdb8e2bac1b3da28c5ed5960de09e59a2fe7e63bb73f5a59e57b0430d2")
    version("4.37.3", sha256="f32ef6ec966cf0e7d2aa88601fed2e3a8f2851c26b5db2c80ccc8f82bee4eedc")
    version("4.31.2", sha256="236b29aee6b113e8f7bee28779c1230a86ad2aac9a74a31b0aedf57e7dfb62a4")
    version("4.29.1", sha256="2b18a172120e32128a80efee04cff487d5d140fe7d817deb648b2eee023a40e4")
    version("4.28.1", sha256="8c8f84131bf04f3b1dcf99b9763cec35c347164ab6ad006e18d2f99fcab05529")
    version("4.26.2", sha256="c1c0e03dd823e9e905232e875ea02dbb2dcd2ba195418c6d11bfaea49b9c774d")

    depends_on("python@3.8:", when="@4.39:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
