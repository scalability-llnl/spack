# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ManDb(AutotoolsPackage):
    """man-db is an implementation of the standard Unix
    documentation system accessed using the man command. It uses
    a Berkeley DB database in place of the traditional
    flat-text whatis databases."""

    homepage = "https://www.nongnu.org/man-db/"
    git = "https://gitlab.com/cjwatson/man-db"
    url = "https://download.savannah.nongnu.org/releases/man-db/man-db-2.10.1.tar.xz"

    license("GPL-2.0-or-later")

    version("2.12.1", sha256="ddee249daeb78cf92bab794ccd069cc8b575992265ea20e239e887156e880265")
    version("2.12.0", sha256="415a6284a22764ad22ff0f66710d853be7790dd451cd71436e3d25c74d996a95")
    version("2.11.2", sha256="cffa1ee4e974be78646c46508e6dd2f37e7c589aaab2938cc1064f058fef9f8d")
    version("2.10.2", sha256="ee97954d492a13731903c9d0727b9b01e5089edbd695f0cdb58d405a5af5514d")
    version("2.10.1", sha256="2ffd8f2e80122fe72e60c740c851e6a3e15c9a7921185eb4752c1c672824bed6")
    version("2.7.6.1", sha256="08edbc52f24aca3eebac429b5444efd48b9b90b9b84ca0ed5507e5c13ed10f3f")

    depends_on("c", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("gettext")
    depends_on("libpipeline@1.5.0:", when="@2.8.0:")
    depends_on("libpipeline@1.4.0:", when="@2.7.1:")
    depends_on("libpipeline@1.3.0:", when="@2.6.7:")
    depends_on("libpipeline@1.1.0:", when="@2.6.0:")
    depends_on("flex")
    depends_on("gdbm")
    depends_on("groff", type=("build", "link", "run"))

    # gnulib bug introduced in commit cbdb5ea63cb5348d9ead16dc46bedda77a4c3d7d.
    # fix is from commit 84863a1c4dc8cca8fb0f6f670f67779cdd2d543b
    patch("gnulib.patch", when="@2.10.2", working_dir="gl")

    # TODO: add gzip support via a new package.
    # man pages are typically compressed, include all available
    # compression libraries
    depends_on("bzip2", type=("build", "link", "run"))
    depends_on("xz", type=("build", "link", "run"))

    def configure_args(self):
        return [
            "--disable-setuid",
            "--without-systemdsystemunitdir",
            "--without-systemdtmpfilesdir",
        ]
