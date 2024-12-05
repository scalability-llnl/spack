# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCantoolz(PythonPackage):
    """CANToolz is a framework for analysing CAN networks and devices.
    It provides multiple modules that can be chained using CANToolz's
    pipe system and used by security researchers, automotive/OEM
    security testers in black-box analysis."""

    homepage = "https://github.com/CANToolz/CANToolz/"
    url = "https://github.com/CANToolz/CANToolz/archive/v3.7.0.tar.gz"

    license("Apache-2.0")

    version("3.7.0", sha256="36f5e8aa407e5c82abe84fb190ddd45ed12887ee833f06ef5eb78504017f0e5d")
    version("3.6.1", sha256="e40c712b726f1caaca16b0d0e0b3aeadd01426944663ba0dce5c47a340304e29")

    depends_on("py-setuptools", type="build")
    depends_on("py-bitstring", type=("build", "run"))
    depends_on("py-flask", type=("build", "run"))
    depends_on("py-pyserial", type=("build", "run"))
    depends_on("py-mido", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
