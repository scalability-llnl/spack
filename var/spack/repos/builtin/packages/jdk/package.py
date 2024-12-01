# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.package import *
from spack.util.prefix import Prefix


class Jdk(Package):
    """The Java Development Kit (JDK) released by Oracle Corporation in the
    form of a binary product aimed at Java developers. Includes a complete JRE
    plus tools for developing, debugging, and monitoring Java applications."""

    homepage = "https://www.oracle.com/technetwork/java/javase/downloads/index.html"

    maintainers("justintoo")

    version(
        "21.0.2",
        sha256="9f1f4a7f25ef6a73255657c40a6d7714f2d269cf15fb2ff1dc9c0c8b56623a6f",
        url="https://download.oracle.com/java/21/latest/jdk-21_linux-x64_bin.tar.gz",
    )
    version(
        "17.0.10",
        sha256="e4fb2df9a32a876afb0a6e17f54c594c2780e18badfa2e8fc99bc2656b0a57b1",
        url="https://download.oracle.com/java/17/latest/jdk-17_linux-x64_bin.tar.gz",
    )

    provides("java@21", when="@21")
    provides("java@17", when="@17")

    requires("target=x86_64:", msg="binaries only availble for x86_64")
    # requires("platform=linux")  # bug in concretizer
    conflicts("platform=windows")
    conflicts("platform=darwin")
    conflicts("platform=freebsd")

    # FIXME:
    # 1. `extends('java')` doesn't work, you need to use `extends('jdk')`
    # 2. Packages cannot extend multiple packages, see #987
    # 3. Update `YamlFilesystemView.merge` to allow a Package to completely
    #    override how it is symlinked into a view prefix. Then, spack activate
    #    can symlink all *.jar files to `prefix.lib.ext`
    extendable = True

    executables = ["^java$"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("-version", output=str, error=str)

        # Make sure this is actually Oracle JDK, not OpenJDK
        if "openjdk" in output:
            return None

        match = re.search(r"\(build (\S+)\)", output)
        return match.group(1).replace("+", "_") if match else None

    @property
    def home(self):
        """Most of the time, ``JAVA_HOME`` is simply ``spec['java'].prefix``.
        However, if the user is using an externally installed JDK, it may be
        symlinked. For example, on macOS, the ``java`` executable can be found
        in ``/usr/bin``, but ``JAVA_HOME`` is actually
        ``/Library/Java/JavaVirtualMachines/jdk-10.0.1.jdk/Contents/Home``.
        Users may not know the actual installation directory and add ``/usr``
        to their ``packages.yaml`` unknowingly. Run ``java_home`` if it exists
        to determine exactly where it is installed. Specify which version we
        are expecting in case multiple Java versions are installed.
        See ``man java_home`` for more details."""

        prefix = self.prefix
        java_home = prefix.libexec.java_home
        if os.path.exists(java_home):
            java_home = Executable(java_home)
            version = str(self.version.up_to(2))
            prefix = java_home("--version", version, output=str).strip()
            prefix = Prefix(prefix)

        return prefix

    @property
    def libs(self):
        """Depending on the version number and whether the full JDK or just
        the JRE was installed, Java libraries can be in several locations:

        * ``lib/libjvm.so``
        * ``jre/lib/libjvm.dylib``

        Search recursively to find the correct library location."""

        return find_libraries(["libjvm"], root=self.home, recursive=True)

    def install(self, spec, prefix):
        install_tree(".", prefix)

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
