# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPerlUnsafeSignals(PerlPackage):
    """Quoting perl581delta:

    In Perl 5.8.0 the so-called "safe signals" were introduced. This means
    that Perl no longer handles signals immediately but instead "between
    opcodes", when it is safe to do so. The earlier immediate handling
    easily could corrupt the internal state of Perl, resulting in
    mysterious crashes.

    It's possible since perl 5.8.1 to globally disable this feature by
    using the PERL_SIGNALS environment variables (as specified in
    "PERL_SIGNALS" in perlrun); but there's no way to disable it locally,
    for a short period of time. That's however something you might want to
    do, if, for example, your Perl program calls a C routine that will
    potentially run for a long time and for which you want to set a
    timeout.

    This module therefore allows you to define UNSAFE_SIGNALS blocks in
    which signals will be handled "unsafely".

    Note that, no matter how short you make the unsafe block, it will still
    be unsafe. Use with caution."""

    homepage = "https://metacpan.org/pod/Perl::Unsafe::Signals"
    url = "https://cpan.metacpan.org/authors/id/R/RG/RGARCIA/Perl-Unsafe-Signals-0.03.tar.gz"

    version("0.03", sha256="d311ae7d73e8d0c2346dfacb82aa952322e70cd928b09d502d739e60e35f829d")
