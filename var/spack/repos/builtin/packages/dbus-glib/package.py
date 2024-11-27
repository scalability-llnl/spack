# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class DbusGlib(AutotoolsPackage):
    """dbus-glib package provides GLib interface for D-Bus API."""

    homepage = "https://dbus.freedesktop.org"
    url = "https://dbus.freedesktop.org/releases/dbus-glib/dbus-glib-0.110.tar.gz"

    license("AFL-2.1 OR GPL-2.0-or-later")

    version("0.112", sha256="7d550dccdfcd286e33895501829ed971eeb65c614e73aadb4a08aeef719b143a")
    version("0.110", sha256="7ce4760cf66c69148f6bd6c92feaabb8812dee30846b24cd0f7395c436d7e825")

    depends_on("c", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("expat")
    depends_on("glib")
    depends_on("dbus")
