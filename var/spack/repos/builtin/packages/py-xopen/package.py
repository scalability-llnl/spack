# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXopen(PythonPackage):
    """This small Python module provides a xopen function that works like the
    built-in open function, but can also deal with compressed files. Supported
    compression formats are gzip, bzip2 and xz. They are automatically
    recognized by their file extensions .gz, .bz2 or .xz."""

    homepage = "https://github.com/pycompression/xopen"
    pypi = "xopen/xopen-0.1.1.tar.gz"

    license("MIT")

    version("1.6.0", sha256="72219a4d690e9c90ad445c45d2119ae2a6d5d38912255631e227aceac6294353")
    version("1.1.0", sha256="38277eb96313b2e8822e19e793791801a1f41bf13ee5b48616a97afc65e9adb3")
    version("1.0.1", sha256="79d7e425fb0930b0153eb6beba9a540ca3e07ac254ca828577ad2e8fa24105dc")
    version("0.9.0", sha256="1e3918c8a5cd2bd128ba05b3b883ee322349219c99c305e10114638478e3162a")
    version("0.8.4", sha256="dcd8f5ef5da5564f514a990573a48a0c347ee1fdbb9b6374d31592819868f7ba")
    version("0.8.2", sha256="003749e09af74103a29e9c64c468c03e084aa6dfe6feff4fe22366679a6534f7")
    version("0.5.0", sha256="b097cd25e8afec42b6e1780c1f6315016171b5b6936100cdf307d121e2cbab9f")
    version("0.1.1", sha256="d1320ca46ed464a59db4c27c7a44caf5e268301e68319f0295d06bf6a9afa6f3")

    depends_on("python@3.7:", type=("build", "run"), when="@1.5.0:")
    depends_on("python@3.6:", type=("build", "run"), when="@1.1.0:")
    depends_on("python@3.5:", type=("build", "run"), when="@0.9.0:")
    depends_on("python@2.7,3.4:", type=("build", "run"), when="@0.5:0.8")
    depends_on("python@2.6:2,3.3:", type=("build", "run"), when="@0.1.1")
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm@6.2:", type="build", when="@1.2.0:")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-isal@1.0.0:", type=("build", "run"), when="@1.6.0: target=x86_64:")
