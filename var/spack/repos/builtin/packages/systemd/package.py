# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Systemd(MesonPackage):
    """systemd is a suite of basic building blocks for a Linux system.
    It provides a system and service manager that runs as PID 1 and
    starts the rest of the system."""

    homepage = "https://systemd.io/"
    url = "https://github.com/systemd/systemd/archive/refs/tags/v255.tar.gz"
    license("GPL-2.0-only")

    version("256.7", sha256="896d76ff65c88f5fd9e42f90d152b0579049158a163431dd77cdc57748b1d7b0")
    version("255", sha256="28854ffb2cb5f9e07fcbdbaf1e03a80b3462a12edeef84893ca2f37b22e4491e")

    depends_on("c", type="build")  # generated

    depends_on("meson@0.60.0:", type="build")
    depends_on("ninja", type="build")
    depends_on("py-jinja2", type="build")
    depends_on("util-linux@2.30:")  # libmount
    depends_on("gperf")
    depends_on("libcap")
    depends_on("pkgconfig")

    conflicts("%gcc@:8.4")
    conflicts("%clang@:7")

    def meson_args(self):
        # Setting prefix is required here because without this the installation
        # prefix would be repeated twice because of the required use of DESTDIR
        # during the install phase.
        # Similarly libdir must be set to prevent the regular prefix path from
        # influencing the placement of the installed files.
        args = [
            "-Dprefix=/",
            "-Dlibdir=/lib",
            "-Dlibidn2=disabled",
            "-Dopenssl=disabled",
            "-Dpcre2=disabled",
            "-Dinitrd=false",
            "-Dresolve=false",
            "-Defi=false",
            "-Dtpm=false",
            "-Dcreate-log-dirs=false",
            "-Dseccomp=disabled",
            "-Dselinux=disabled",
            "-Dapparmor=disabled",
            "-Dsmack=false",
            "-Dpolkit=disabled",
            "-Dima=false",
            "-Dacl=disabled",
            "-Daudit=disabled",
            "-Dblkid=disabled",
            "-Dfdisk=disabled",
            "-Dkmod=false",
            "-Dpam=disabled",
            "-Dpasswdqc=disabled",
            "-Dpwquality=disabled",
            "-Dmicrohttpd=disabled",
            "-Dlibcryptsetup=disabled",
            "-Dlibcurl=disabled",
            "-Dlibiptc=disabled",
            "-Dqrencode=disabled",
            "-Dgcrypt=disabled",
            "-Dgnutls=disabled",
            "-Dp11kit=disabled",
            "-Dlibfido2=disabled",
            "-Dtpm2=disabled",
            "-Delfutils=disabled",
            "-Dzlib=disabled",
            "-Dbzip2=disabled",
            "-Dxz=disabled",
            "-Dlz4=disabled",
            "-Dzstd=disabled",
            "-Dxkbcommon=disabled",
            "-Dbootloader=disabled",
            "-Dnscd=false",  # support for...
            "-Dutmp=false",
            "-Dhibernate=false",
            "-Dldconfig=false",
            "-Denvironment-d=false",
            "-Dbinfmt=false",
            "-Dremote=disabled",
            "-Dfirstboot=false",
            "-Drandomseed=false",
            "-Dbacklight=false",
            "-Dvconsole=false",
            "-Dvmspawn=disabled",
            "-Dquotacheck=false",
            "-Dsysusers=false",
            "-Dstoragetm=false",
            "-Dtmpfiles=false",
            "-Dimportd=disabled",
            "-Dhwdb=false",
            "-Drfkill=false",
            "-Dgshadow=false",
            "-Dkmod=disabled",
            "-Dxenctrl=disabled",
            "-Drepart=disabled",  # install the...
            "-Dsysupdate=disabled",
            "-Dcoredump=false",
            "-Dpstore=false",
            "-Doomd=false",
            "-Dlogind=false",
            "-Dhostnamed=false",
            "-Dlocaled=false",
            "-Dmachined=false",
            "-Dportabled=false",
            "-Dsysext=false",
            "-Duserdb=false",
            "-Dhomed=disabled",
            "-Dnetworkd=false",
            "-Dtimedated=false",
            "-Dtimesyncd=false",
            "-Dxdg-autostart=false",
            "-Ddefault-network=false",  # install...
            "-Dnss-myhostname=false",
            "-Dnss-mymachines=disabled",
            "-Dnss-resolve=disabled",
            "-Dnss-systemd=false",
            "-Dhtml=disabled",
            "-Dtranslations=false",
            "-Dinstall-sysconfdir=false",
            "-Dkernel-install=false",
            "-Dukify=disabled",
            "-Danalyze=false",
        ]

        return args

    def install(self, spec, prefix):
        # DESTDIR is required because without it the install phase will attempt
        # to install files in the root file system by default.
        os.environ["DESTDIR"] = prefix
        with working_dir(self.build_directory):
            ninja("install")
