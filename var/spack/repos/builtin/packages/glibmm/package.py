# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Glibmm(AutotoolsPackage):
    """Glibmm is a C++ wrapper for the glib library."""

    homepage = "https://developer.gnome.org/glib/"
    url      = "https://ftp.gnome.org/pub/GNOME/sources/glibmm/2.19/glibmm-2.19.3.tar.gz"

    version('2.19.3', sha256='23958368535c19188b1241c4615dcf1f35e80e0922a04236bb9247dcd8fe0a2b')
    version('2.16.0', sha256='99795b9c6e58e490df740a113408092bf47a928427cbf178d77c35adcb6a57a3')
    version('2.4.8', sha256='78b97bfa1d001cc7b398f76bf09005ba55b45ae20780b297947a1a71c4f07e1f')

    depends_on('libsigcpp')
    depends_on('glib')

    patch('guint16_cast.patch', when='@2.19.3')

    def url_for_version(self, version):
        """Handle glibmm's version-based custom URLs."""
        url = "https://ftp.acc.umu.se/pub/GNOME/sources/glibmm"
        ext = '.tar.gz' if version < Version('2.28.2') else '.tar.xz'
        return url + "/%s/glibmm-%s%s" % (version.up_to(2), version, ext)
