# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class XkeyboardConfig(AutotoolsPackage, XorgPackage):
    """This project provides a consistent, well-structured, frequently
    released, open source database of keyboard configuration data. The
    project is targeted to XKB-based systems."""

    homepage = "https://www.freedesktop.org/wiki/Software/XKeyboardConfig/"
    xorg_mirror_path = "data/xkeyboard-config/xkeyboard-config-2.18.tar.gz"

    license("MIT")

    version("2.34", sha256="a5882238b4199ca90428aea102790aaa847e6e214653d956bf2abba3027107ba")
    version("2.18", sha256="d5c511319a3bd89dc40622a33b51ba41a2c2caad33ee2bfe502363fcc4c3817d")

    depends_on("libx11@1.4.3:")

    depends_on("libxslt", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("intltool@0.30:", type="build")
    depends_on("xproto@7.0.20:", type="build")

    # TODO: missing dependencies
    # xgettext
    # msgmerge
    # msgfmt
    # gmsgfmt
    # perl@5.8.1:
    # perl XML::Parser

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("XKB_CONFIG_ROOT", self.prefix.share.X11.xkb)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path("XKB_CONFIG_ROOT", self.prefix.share.X11.xkb)
