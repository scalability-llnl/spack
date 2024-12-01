# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAddict(PythonPackage):
    """addict is a Python module that gives you dictionaries
    whose values are both gettable and settable using
    attributes, in addition to standard item-syntax."""

    homepage = "https://github.com/mewwts/addict"
    url = "https://github.com/mewwts/addict/archive/v2.2.1.tar.gz"

    license("MIT")

    version("2.2.1", sha256="398bba9e7fa25e2ce144c5c4b8ec6208e89b9445869403dfa88ab66ec110fa12")

    depends_on("py-setuptools", type="build")
