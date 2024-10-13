# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Icedtea(AutotoolsPackage):
    """The IcedTea project provides a harness to build the source code from
    https://openjdk.java.net/ using Free Software build tools and adds a number
    of key features to the upstream OpenJDK codebase. IcedTea requires an
    existing IcedTea or OpenJDK install to build."""

    homepage = "https://openjdk.java.net/projects/icedtea/"
    url = "https://icedtea.wildebeest.org/download/source/icedtea-3.4.0.tar.gz"

    license("GPL-2.0-or-later")

    version("3.9.0", sha256="84a63bc59f4e101ce8fa183060a59c7e8cbe270945310e90c92b8609a9b8bc88")
    version("3.8.0", sha256="ef1a9110294d0a905833f1db30da0c8a88bd2bde8d92ddb711d72ec763cd25b0")
    version("3.7.0", sha256="936302694e193791885e81cf72097eeadee5b68ba220889228b0aafbfb2cb654")
    version("3.6.0", sha256="74a43c4e027c72bb1c324f8f73af21565404326c9998f534f234ec2a36ca1cdb")
    version("3.5.1", sha256="b229f2aa5d743ff850fa695e61f65139bb6eca1a9d10af5306ad3766fcea2eb2")
    version("3.5.0", sha256="2c92e18fa70edaf73517fcf91bc2a7cc2ec2aa8ffdf22bb974fa6f9bc3065f30")
    version("3.4.0", sha256="2b606bbbf4ca5bcf2c8e811ea9060da30744860f3d63e1b3149fb5550a90b92b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("X", default=False, description="Build with GUI support.")
    variant(
        "shenandoah",
        default=False,
        description="Build with the shenandoah gc. Only for version 3+",
    )

    depends_on("pkgconfig", type="build")
    depends_on("gmake", type="build")
    depends_on("cups")
    depends_on("java", type="build")
    # X11 deps required for building even when headless
    depends_on("libx11", when="~X", type="build")
    depends_on("xproto", when="~X", type="build")
    depends_on("libxext", when="~X", type="build")
    depends_on("libxtst", when="~X", type="build")
    depends_on("libxi", when="~X", type="build")
    depends_on("libxt", when="~X", type="build")
    depends_on("libxinerama", when="~X", type="build")
    depends_on("libxrender", when="~X", type="build")
    depends_on("libxcomposite", when="~X", type="build")
    depends_on("libxau", when="~X", type="build")
    depends_on("libxdmcp", when="~X", type="build")
    depends_on("gtkplus", when="~X", type="build")

    depends_on("libx11", when="+X")
    depends_on("xproto", when="+X")
    depends_on("libxext", when="+X")
    depends_on("libxtst", when="+X")
    depends_on("libxi", when="+X")
    depends_on("libxt", when="+X")
    depends_on("libxinerama", when="+X")
    depends_on("libxrender", when="+X")
    depends_on("libxcomposite", when="+X")
    depends_on("libxau", when="+X")
    depends_on("libxdmcp", when="+X")
    depends_on("gtkplus", when="+X")

    depends_on("freetype@2:")
    depends_on("wget", type="build")
    depends_on("giflib")
    depends_on("libpng")
    depends_on("jpeg")
    depends_on("lcms")
    depends_on("zlib-api")
    depends_on("alsa-lib", when="platform=linux")

    provides("java@8", when="@3.4.0:3")

    force_autoreconf = True

    resource(
        name="corba",
        placement="corba_src",
        sha256="47210b6c69dcc6193b9bf0a3d61b75b48f4fa56e8ca348e40200cfa14eca3fd1",
        url="https://icedtea.wildebeest.org/download/drops/icedtea8/3.4.0/corba.tar.xz",
        when="@3.4.0",
    )
    resource(
        name="hotspot",
        placement="hotspot_src",
        sha256="973d668f312b869184665def8abe4037dcd78562bf0dda40367102aca647fd76",
        url="https://icedtea.wildebeest.org/download/drops/icedtea8/3.4.0/hotspot.tar.xz",
        when="@3.4.0",
    )
    resource(
        name="jaxp",
        placement="jaxp_src",
        sha256="c74a8a27f1d2dfeaabfce3b5b46623e367fb0fbd5938a3aca8fcd23eb2ce1d53",
        url="https://icedtea.wildebeest.org/download/drops/icedtea8/3.4.0/jaxp.tar.xz",
        when="@3.4.0",
    )
    resource(
        name="jaxws",
        placement="jaxws_src",
        sha256="90642e9131f4c8922576305224278fcae72d8363956b76d4cdbf813027836cac",
        url="https://icedtea.wildebeest.org/download/drops/icedtea8/3.4.0/jaxws.tar.xz",
        when="@3.4.0",
    )
    resource(
        name="jdk",
        placement="jdk_src",
        sha256="ec71e37b98b4baa6831c5cb30bcc1ab18cd95993744dbc4d37a28b2dc5049896",
        url="https://icedtea.wildebeest.org/download/drops/icedtea8/3.4.0/jdk.tar.xz",
        when="@3.4.0",
    )
    resource(
        name="langtools",
        placement="langtools_src",
        sha256="489799c6a86fbfb7da2f2c0ec48e44970a152ea38b97bb40cc04bc09155ab39f",
        url="https://icedtea.wildebeest.org/download/drops/icedtea8/3.4.0/langtools.tar.xz",
        when="@3.4.0",
    )
    resource(
        name="openjdk",
        placement="openjdk_src",
        sha256="f1eb8c8e45965adcaa1e9cc70df043a825d52409e96712d266167994ff88456d",
        url="https://icedtea.wildebeest.org/download/drops/icedtea8/3.4.0/openjdk.tar.xz",
        when="@3.4.0",
    )
    resource(
        name="nashorn",
        placement="nashorn_src",
        sha256="3f3861e7268a3986fa8d5c940b85a0de1003f7ebb212df157a9b421ac621d6ae",
        url="https://icedtea.wildebeest.org/download/drops/icedtea8/3.4.0/nashorn.tar.xz",
        when="@3.4.0",
    )
    resource(
        name="shenandoah",
        placement="shenandoah_src",
        sha256="61f7cc5896791ae564aa365cb3de80b16426b42f07e5734ebd30c4483fa2fd3a",
        url="https://icedtea.wildebeest.org/download/drops/icedtea8/3.4.0/shenandoah.tar.xz",
        when="@3.4.0",
    )

    # FIXME:
    # 1. `extends('java')` doesn't work, you need to use `extends('icedtea')`
    # 2. Packages cannot extend multiple packages, see #987
    # 3. Update `YamlFilesystemView.merge` to allow a Package to completely
    #    override how it is symlinked into a view prefix. Then, spack activate
    #    can symlink all *.jar files to `prefix.lib.ext`
    extendable = True

    def configure_args(self):
        os.environ["POTENTIAL_CXX"] = os.environ["CXX"]
        os.environ["POTENTIAL_CC"] = os.environ["CC"]
        os.environ["WGET"] = self.spec["wget"].command.path
        args = []
        if self.spec.satisfies("~X"):
            args.append("--enable-headless")
        if self.spec.satisfies("+shenandoah"):
            args.append("--with-hotspot-build=shenandoah")
            args.append("--with-hotspot-src-zip=" + self.stage[9].archive_file)
            args.append("--with-hotspot-checksum=no")
        else:
            args.append("--with-hotspot-src-zip=" + self.stage[2].archive_file)
            args.append("--with-hotspot-checksum=no")
        args += [
            "--with-corba-src-zip=" + self.stage[1].archive_file,
            "--with-cobra-checksum=no",
            "--with-jaxp-src-zip=" + self.stage[3].archive_file,
            "--with-jaxp-checksum=no",
            "--with-jaxws-src-zip=" + self.stage[4].archive_file,
            "--with-jaxws-checksum=no",
            "--with-jdk-src-zip=" + self.stage[5].archive_file,
            "--with-jdk-checksum=no",
            "--with-langtools-src-zip=" + self.stage[6].archive_file,
            "--with-langtools-checksum=no",
            "--with-openjdk-src-zip=" + self.stage[7].archive_file,
            "--with-openjdk-checksum=no",
            "--with-nashorn-src-zip=" + self.stage[8].archive_file,
            "--with-nashorn-checksum=no",
            "--disable-maintainer-mode" "--disable-downloading",
            "--disable-system-pcsc",
            "--disable-system-sctp",
            "--disable-system-kerberos",
            "--with-jdk-home=" + self.spec["jdk"].home,
        ]
        return args

    def setup_run_environment(self, env):
        """Set JAVA_HOME."""

        env.set("JAVA_HOME", self.home)

    def setup_dependent_build_environment(self, env, dependent_spec):
        """Set JAVA_HOME and CLASSPATH.

        CLASSPATH contains the installation prefix for the extension and any
        other Java extensions it depends on."""

        env.set("JAVA_HOME", self.home)

        class_paths = []
        for d in dependent_spec.traverse(deptype=("build", "run", "test")):
            if d.package.extends(self.spec):
                class_paths.extend(find(d.prefix, "*.jar"))

        classpath = os.pathsep.join(class_paths)
        env.set("CLASSPATH", classpath)

    def setup_dependent_run_environment(self, env, dependent_spec):
        """Set CLASSPATH.

        CLASSPATH contains the installation prefix for the extension and any
        other Java extensions it depends on."""
        # For runtime environment set only the path for
        # dependent_spec and prepend it to CLASSPATH
        if dependent_spec.package.extends(self.spec):
            class_paths = find(dependent_spec.prefix, "*.jar")
            classpath = os.pathsep.join(class_paths)
            env.prepend_path("CLASSPATH", classpath)
