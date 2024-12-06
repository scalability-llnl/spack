# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RProto(RPackage):
    """Prototype Object-Based Programming.

    An object oriented system using object-based, also called prototype-based,
    rather than class-based object oriented ideas."""

    cran = "proto"

    license("GPL-2.0-only")

    version("1.0.0", sha256="9294d9a3b2b680bb6fac17000bfc97453d77c87ef68cfd609b4c4eb6d11d04d1")
    version("0.3-10", sha256="d0d941bfbf247879b3510c8ef3e35853b1fbe83ff3ce952e93d3f8244afcbb0e")
