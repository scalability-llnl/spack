# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xdm(AutotoolsPackage, XorgPackage):
    """X Display Manager / XDMCP server."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xdm"
    xorg_mirror_path = "app/xdm-1.1.11.tar.gz"

    license("MIT")

    version("1.1.16", sha256="931013642b7fab893f374eb1aa6f9ad043c88b654802fc51f841cea76aff44e0")
    version("1.1.14", sha256="bcc543c3c120094d58d9cc9837958d4303693c2116ba342ba3dd9440137b4026")
    version("1.1.13", sha256="2f05aa58c205dcf10443ba414d27535b74ec11466dc95228343b0ce4f0c2a307")
    version("1.1.12", sha256="8ea737945f69e172afbbc8b5060e4c7ea8079f402eb0a458572197c907020bb4")
    version("1.1.11", sha256="38c544a986143b1f24566c1a0111486b339b92224b927be78714eeeedca12a14")

    depends_on("c", type="build")  # generated

    depends_on("libxmu")
    depends_on("libx11")
    depends_on("libxau")
    depends_on("libxinerama")
    depends_on("libxft")
    depends_on("libxpm")
    depends_on("libxaw")
    depends_on("libxdmcp")
    depends_on("libxt")
    depends_on("libxext")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
