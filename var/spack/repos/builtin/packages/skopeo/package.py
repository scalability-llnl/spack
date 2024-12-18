# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Skopeo(MakefilePackage):
    """skopeo is a command line utility that performs various operations on
    container images and image repositories."""

    homepage = "https://github.com/containers/skopeo"
    url = "https://github.com/containers/skopeo/archive/v0.1.39.tar.gz"

    license("Apache-2.0")

    version("0.1.40", sha256="ee1e33245938fcb622f5864fac860e2d8bfa2fa907af4b5ffc3704ed0db46bbf")
    version("0.1.39", sha256="e9d70f7f7b891675a816f06a22df0490285ad20eefbd91f5da69ca12f56c29f2")
    version("0.1.38", sha256="104ceb9c582dc5c3a49dd1752c4c326bba03f2f801596f089372e831f48ed705")
    version("0.1.37", sha256="49c0c1b2c2f32422d3230f827ae405fc554fb34af41a54e59b2121ac1500505d")
    version("0.1.36", sha256="42f9b0bf53ae44bc294be400e2c5259f977ffa4d5dbac3576b0b5e23d59791fd")

    depends_on("c", type="build")  # generated

    depends_on("go")
    depends_on("go-md2man", type="build")
    depends_on("gpgme")
    depends_on("libassuan")
    depends_on("libgpg-error")
    depends_on("lvm2")

    def edit(self, spec, prefix):
        grep = which("grep")
        files = grep(
            "-lR",
            "/etc/containers/",
            "vendor",
            output=str,
            env={"PATH": "/usr/bin:/bin:/usr/sbin:/sbin"},
        )

        for f in files.splitlines():
            edit = FileFilter(f)
            edit.filter("/etc/containers/", "{0}/etc/containers/".format(prefix))

    def build(self, spec, prefix):
        make("binary-local")

    def install(self, spec, prefix):
        make("binary-local", "install", "DESTDIR={0}".format(prefix), "PREFIX={0}".format(prefix))
