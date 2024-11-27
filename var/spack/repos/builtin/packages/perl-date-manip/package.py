# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDateManip(PerlPackage):
    """Date::Manip - Date manipulation routines

    Date::Manip is a series of modules designed to make any common date/time
    operation easy to do. Operations such as comparing two times,
    determining a date a given amount of time from another, or parsing
    international times are all easily done. It deals with time as it is
    used in the Gregorian calendar (the one currently in use) with full
    support for time changes due to daylight saving time."""

    homepage = "https://metacpan.org/release/Date-Manip"
    url = "https://cpan.metacpan.org/authors/id/S/SB/SBECK/Date-Manip-6.82.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("6.91", sha256="6bd9cb47e82ba91fdba4022ef358149d81e8453f52ca54f49faac2696210c479")
    version("6.82", sha256="fa96bcf94c6b4b7d3333f073f5d0faad59f546e5aec13ac01718f2e6ef14672a")
