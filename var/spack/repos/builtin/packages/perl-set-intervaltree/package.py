# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSetIntervaltree(PerlPackage):
    """Set::IntervalTree uses Interval Trees to store and efficiently look up
    ranges using a range-based lookup."""

    homepage = "https://metacpan.org/release/Set-IntervalTree"
    url = "https://cpan.metacpan.org/authors/id/B/BE/BENBOOTH/Set-IntervalTree-0.10.tar.gz"

    version("0.10", sha256="e3bd9ccf0d074b5f879eef1ed88254983697bf83d02744fce62150ee46553ebc")

    depends_on("cxx", type="build")  # generated

    depends_on("perl-extutils-makemaker", type="build")
