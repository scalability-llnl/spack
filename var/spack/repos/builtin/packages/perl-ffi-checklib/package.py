# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlFfiChecklib(PerlPackage):
    """This module checks whether a particular dynamic library is available for
    FFI to use. It is modeled heavily on Devel::CheckLib, but will find dynamic
    libraries even when development packages are not installed. It also
    provides a find_lib function that will return the full path to the found
    dynamic library, which can be feed directly into FFI::Platypus or another
    FFI system."""

    homepage = "https://metacpan.org/pod/FFI::CheckLib"
    url = "https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/FFI-CheckLib-0.25.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.31", sha256="04d885fc377d44896e5ea1c4ec310f979bb04f2f18658a7e7a4d509f7e80bb80")
    version("0.25", sha256="eb36b9a7cff1764a65b1b77e01e92c26207c558a3f986d0d17d2b110fa366ba4")
