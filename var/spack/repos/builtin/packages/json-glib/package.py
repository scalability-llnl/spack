# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class JsonGlib(AutotoolsPackage):
    """JSON-GLib is a library for reading and parsing JSON using GLib and
    GObject data types and API."""

    homepage = "https://developer.gnome.org/json-glib"
    url      = "https://ftp.gnome.org/pub/gnome/sources/json-glib/1.2/json-glib-1.2.8.tar.xz"

    version('1.2.8', sha256='fd55a9037d39e7a10f0db64309f5f0265fa32ec962bf85066087b83a2807f40a')

    depends_on('glib')
