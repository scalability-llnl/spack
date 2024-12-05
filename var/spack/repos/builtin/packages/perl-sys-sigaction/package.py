# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSysSigaction(PerlPackage):
    """Prior to version 5.8.0 perl implemented 'unsafe' signal handling. The
    reason it is consider unsafe, is that there is a risk that a signal will
    arrive, and be handled while perl is changing internal data structures.
    This can result in all kinds of subtle and not so subtle problems. For this
    reason it has always been recommended that one do as little as possible in
    a signal handler, and only variables that already exist be manipulated.

    Perl 5.8.0 and later versions implements 'safe' signal handling on
    platforms which support the POSIX sigaction() function. This is
    accomplished by having perl note that a signal has arrived, but deferring
    the execution of the signal handler until such time as it is safe to do so.
    Unfortunately these changes can break some existing scripts, if they
    depended on a system routine being interrupted by the signal's arrival. The
    perl 5.8.0 implementation was modified further in version 5.8.2"""

    homepage = "https://metacpan.org/pod/Sys::SigAction"
    url = "https://cpan.metacpan.org/authors/id/L/LB/LBAXTER/Sys-SigAction-0.23.tar.gz"

    version("0.23", sha256="c4ef6c9345534031fcbbe2adc347fc7194d47afc945e7a44fac7e9563095d353")
