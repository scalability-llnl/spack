# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlIoStringy(PerlPackage):
    """This toolkit primarily provides modules for performing both traditional
    and object-oriented i/o) on things other than normal filehandles; in
    particular, IO::Scalar, IO::ScalarArray, and IO::Lines.

    In the more-traditional IO::Handle front, we have IO::AtomicFile which may
    be used to painlessly create files which are updated atomically.

    And in the "this-may-prove-useful" corner, we have IO::Wrap, whose exported
    wraphandle() function will clothe anything that's not a blessed object in
    an IO::Handle-like wrapper... so you can just use OO syntax and stop
    worrying about whether your function's caller handed you a string, a
    globref, or a FileHandle."""

    homepage = "https://metacpan.org/pod/IO::Stringy"
    url = "https://cpan.metacpan.org/authors/id/C/CA/CAPOEIRAB/IO-Stringy-2.112.tar.gz"

    version("2.113", sha256="51220fcaf9f66a639b69d251d7b0757bf4202f4f9debd45bdd341a6aca62fe4e")
    version("2.111", sha256="8c67fd6608c3c4e74f7324f1404a856c331dbf48d9deda6aaa8296ea41bf199d")

    def url_for_version(self, version):
        if self.spec.satisfies("@2.112:"):
            return (
                f"https://cpan.metacpan.org/authors/id/C/CA/CAPOEIRAB/IO-Stringy-{version}.tar.gz"
            )
        else:
            return f"https://cpan.metacpan.org/authors/id/D/DS/DSKOLL/IO-stringy-{version}.tar.gz"
