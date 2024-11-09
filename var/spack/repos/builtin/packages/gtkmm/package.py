# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gtkmm(AutotoolsPackage):
    """Gtkmm is the official C++ interface for the popular GUI library GTK+."""

    homepage = "https://www.gtkmm.org/en/"
    url = "https://ftp.acc.umu.se/pub/GNOME/sources/gtkmm/2.16/gtkmm-2.16.0.tar.gz"

    license("LGPL-2.1-or-later")

    version("2.19.7", sha256="7cc8d26f9a0956092e61ecfbb029c5d6223cd7e49d4434653446ff190a990957")
    version("2.19.6", sha256="d495d4012d49841a4f0a09584e002bc25ef55d7b2782660ecf7a58ed67357ad7")
    version("2.19.4", sha256="ade220b0d395cb44215a69623af40a420281bc090ddaefc55350ad48e888fed2")
    version("2.19.2", sha256="9c152f2d652344d9000756491c6b00bd394162f57f4302524db8535144b397a0")
    version("2.17.11", sha256="0ec15d7aa14a0528352adf91aa612079590ba377aa15f47f7c8d37611ffbfbcd")
    version("2.17.1", sha256="bd1369caeb28ffdc9e81b1c4dc846c265dd9533bed7958756b3ee4d14ffa1694")
    version("2.16.0", sha256="7b2cccda794531ecfa65c01e57614ecba526153ad2a29d580c6e8df028d56ec4")
    version("2.4.11", sha256="0754187a5bcf3795cd7c959de303e6a19a130b0c5927bff1504baa3524bee8c1")

    depends_on("cxx", type="build")  # generated

    depends_on("glibmm")
    depends_on("atk")
    depends_on("gtkplus")
    depends_on("pangomm")
    depends_on("cairomm")
    depends_on("pkgconfig", type="build")

    def url_for_version(self, version):
        """Handle glib's version-based custom URLs."""
        url = "https://ftp.acc.umu.se/pub/GNOME/sources/gtkmm"
        ext = ".tar.gz" if version < Version("3.1.0") else ".tar.xz"
        return url + "/%s/gtkmm-%s%s" % (version.up_to(2), version, ext)
