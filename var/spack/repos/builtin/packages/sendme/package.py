#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sendme(CargoPackage):
    """A cli tool to send directories over the network, with NAT hole punching"""

    homepage = "https://www.iroh.computer/sendme"
    git = "https://github.com/n0-computer/sendme.git"

    maintainers("draguve")

    license("Apache-2.0 OR MIT")

    version("main", branch="main")
    version("0.23.0", tag="v0.23.0", commit="39f6111d8c3a973ea1f54a3c47aad07014de854b")

    sanity_check_is_file = [join_path("bin", "sendme")]
