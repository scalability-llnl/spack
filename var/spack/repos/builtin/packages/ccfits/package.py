# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ccfits(AutotoolsPackage):
    """CCfits is an object oriented interface to the cfitsio library.
    It is designed to make the capabilities of cfitsio available to programmers
    working in C++. It is written in ANSI C++ and implemented using the C++
    Standard Library with namespaces, exception handling, and member template
    functions."""

    homepage = "https://heasarc.gsfc.nasa.gov/fitsio/CCfits/"
    url = "https://heasarc.gsfc.nasa.gov/fitsio/CCfits/CCfits-2.5.tar.gz"

    version("2.6", sha256="2bb439db67e537d0671166ad4d522290859e8e56c2f495c76faa97bc91b28612")
    version("2.5", sha256="938ecd25239e65f519b8d2b50702416edc723de5f0a5387cceea8c4004a44740")
    version("2.4", sha256="ba6c5012b260adf7633f92581279ea582e331343d8c973981aa7de07242bd7f8")

    depends_on("cxx", type="build")  # generated

    depends_on("cfitsio")
