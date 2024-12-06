# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlIoAll(PerlPackage):
    """IO::All combines all of the best Perl IO modules into a single nifty
    object oriented interface to greatly simplify your everyday Perl IO idioms.
    It exports a single function called io, which returns a new IO::All object.
    And that object can do it all!

    The IO::All object is a proxy for IO::File, IO::Dir, IO::Socket, Tie::File,
    File::Spec, File::Path, File::MimeInfo and File::ReadBackwards; as well as
    all the DBM and MLDBM modules. You can use most of the methods found in
    these classes and in IO::Handle (which they inherit from). IO::All adds
    dozens of other helpful idiomatic methods including file stat and
    manipulation functions.

    IO::All is pluggable, and modules like IO::All::LWP and IO::All::Mailto add
    even more functionality. Optionally, every IO::All object can be tied to
    itself. This means that you can use most perl IO builtins on it: readline,
    <>, getc, print, printf, syswrite, sysread, close."""

    homepage = "https://metacpan.org/pod/distribution/IO-All/lib/IO/All.pod"
    url = "https://cpan.metacpan.org/authors/id/F/FR/FREW/IO-All-0.87.tar.gz"

    license("Artistic-1.0")

    version("0.87", sha256="54e21d250c0229127e30b77a3461e10077854ec244f26fb670f1b445ed4c4d5b")
