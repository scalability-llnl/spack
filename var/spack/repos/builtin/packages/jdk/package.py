# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

import llnl.util.tty as tty
from spack.package import *
from spack.util.prefix import Prefix


class Jdk(Package):
    """The Java Development Kit (JDK) released by Oracle Corporation in the
    form of a binary product aimed at Java developers. Includes a complete JRE
    plus tools for developing, debugging, and monitoring Java applications."""

    homepage = "http://www.oracle.com/technetwork/java/javase/downloads/index.html"

    maintainers = ['justintoo']

    # Oracle requires that you accept their License Agreement in order
    # to access the Java packages in download.oracle.com. In order to
    # automate this process, we need to utilize these additional curl
    # command-line options. See:
    # http://stackoverflow.com/questions/10268583/how-to-automate-download-and-installation-of-java-jdk-on-linux
    fetch_options = {'cookie': 'oraclelicense=accept-securebackup-cookie'}

    # To add the latest version, go to the homepage listed above,
    # click "JDK Download", click "Accept License Agreement", right-click the
    # Linux .tar.gz link, and select Copy Link Address. The checksum can be
    # found in a link above. The build number can be deciphered from the URL.
    # Alternatively, run `bin/java -version` after extracting. Replace '+'
    # symbol in version with '_', otherwise it will be interpreted as a variant
    version('14_36', sha256='4639bbaecc9cc606f1a4b99fda1efcaefcbf57a7025b3828b095093a6c866afd',
            url='https://download.oracle.com/otn-pub/java/jdk/14+36/076bab302c7b4508975440c56f6cc26a/jdk-14_linux-x64_bin.tar.gz')
    version('12.0.2_10', sha256='2dde6fda89a4ec6e6560ed464e917861c9e40bf576e7a64856dafc55abaaff51',
            url='https://download.oracle.com/otn-pub/java/jdk/12.0.2+10/e482c34c86bd4bf8b56c0b35558996b9/jdk-12.0.2_linux-x64_bin.tar.gz')
    version('12.0.1_12', sha256='9fd6dcdaf2cfca7da59e39b009a0f5bcd53bec2fb16105f7ca8d689cdab68d75',
            url='https://download.oracle.com/otn-pub/java/jdk/12.0.1+12/69cfe15208a647278a19ef0990eea691/jdk-12.0.1_linux-x64_bin.tar.gz')
    version('11.0.2_9', sha256='7b4fd8ffcf53e9ff699d964a80e4abf9706b5bdb5644a765c2b96f99e3a2cdc8',
            url='https://download.oracle.com/otn-pub/java/jdk/11.0.2+9/f51449fcd52f4d52b93a989c5c56ed3c/jdk-11.0.2_linux-x64_bin.tar.gz')
    version('11.0.1_13', sha256='e7fd856bacad04b6dbf3606094b6a81fa9930d6dbb044bbd787be7ea93abc885',
            url='https://download.oracle.com/otn-pub/java/jdk/11.0.1+13/90cf5d8f270a4347a95050320eef3fb7/jdk-11.0.1_linux-x64_bin.tar.gz')
    version('10.0.2_13', sha256='6633c20d53c50c20835364d0f3e172e0cbbce78fff81867488f22a6298fa372b',
            url='https://download.oracle.com/otn-pub/java/jdk/10.0.2+13/19aef61b38124481863b1413dce1855f/jdk-10.0.2_linux-x64_bin.tar.gz')
    version('10.0.1_10', sha256='ae8ed645e6af38432a56a847597ac61d4283b7536688dbab44ab536199d1e5a4',
            url='https://download.oracle.com/otn-pub/java/jdk/10.0.1+10/fb4372174a714e6b8c52526dc134031e/jdk-10.0.1_linux-x64_bin.tar.gz')
    version('1.8.0_241-b07', sha256='419d32677855f676076a25aed58e79432969142bbd778ff8eb57cb618c69e8cb',
            url='https://download.oracle.com/otn-pub/java/jdk/8u241-b07/1f5b5a70bf22433b84d0e960903adac8/jdk-8u241-linux-x64.tar.gz')
    version('1.8.0_231-b11', sha256='a011584a2c9378bf70c6903ef5fbf101b30b08937441dc2ec67932fb3620b2cf',
            url='https://download.oracle.com/otn-pub/java/jdk/8u231-b11/5b13a193868b4bf28bcb45c792fce896/jdk-8u231-linux-x64.tar.gz')
    version('1.8.0_212-b10', sha256='3160c50aa8d8e081c8c7fe0f859ea452922eca5d2ae8f8ef22011ae87e6fedfb',
            url='https://download.oracle.com/otn-pub/java/jdk/8u212-b10/59066701cf1a433da9770636fbc4c9aa/jdk-8u212-linux-x64.tar.gz')
    version('1.8.0_202-b08', sha256='9a5c32411a6a06e22b69c495b7975034409fa1652d03aeb8eb5b6f59fd4594e0',
            url='https://download.oracle.com/otn-pub/java/jdk/8u202-b08/1961070e4c9b4e26a04e7f5a083f551e/jdk-8u202-linux-x64.tar.gz')
    version('1.8.0_141-b15', sha256='041d5218fbea6cd7e81c8c15e51d0d32911573af2ed69e066787a8dc8a39ba4f',
            url='https://download.oracle.com/otn-pub/java/jdk/8u141-b15/336fa29ff2bb4ef291e347e091f7f4a7/jdk-8u141-linux-x64.tar.gz')
    version('1.8.0_131-b11', sha256='62b215bdfb48bace523723cdbb2157c665e6a25429c73828a32f00e587301236',
            url='https://download.oracle.com/otn-pub/java/jdk/8u131-b11/d54c1d3a095b4ff2b6607d096fa80163/jdk-8u131-linux-x64.tar.gz')

    provides('java@14', when='@14.0:14.999')
    provides('java@13', when='@13.0:13.999')
    provides('java@12', when='@12.0:12.999')
    provides('java@11', when='@11.0:11.999')
    provides('java@10', when='@10.0:10.999')
    provides('java@9',  when='@9.0:9.999')
    provides('java@8',  when='@1.8.0:1.8.999')
    provides('java@7',  when='@1.7.0:1.7.999')

    conflicts('target=ppc64:', msg='jdk is only available for x86_64')
    conflicts('target=ppc64le:', msg='jdk is only available for x86_64')

    # FIXME:
    # 1. `extends('java')` doesn't work, you need to use `extends('jdk')`
    # 2. Packages cannot extend multiple packages, see #987
    # 3. Update `YamlFilesystemView.merge` to allow a Package to completely
    #    override how it is symlinked into a view prefix. Then, spack activate
    #    can symlink all *.jar files to `prefix.lib.ext`
    extendable = True

    executables = ['^java$']

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('-version', output=str, error=str)

        # Make sure this is actually Oracle JDK, not OpenJDK
        if 'openjdk' in output:
            return None

        match = re.search(r'\(build (\S+)\)', output)
        return match.group(1).replace('+', '_') if match else None

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
            prefix = java_home('--version', version, output=str).strip()
            prefix = Prefix(prefix)

        return prefix

    @property
    def libs(self):
        """Depending on the version number and whether the full JDK or just
        the JRE was installed, Java libraries can be in several locations:

        * ``lib/libjvm.so``
        * ``jre/lib/libjvm.dylib``

        Search recursively to find the correct library location."""

        return find_libraries(['libjvm'], root=self.home, recursive=True)

    @run_before('install')
    def macos_check(self):
        if self.spec.satisfies('platform=darwin'):
            msg = """\
Spack's JDK package only supports Linux. If you need to install JDK on macOS,
manually download the .dmg from:

    {0}

and double-click to install. Once JDK is installed, you can tell Spack where
to find it like so. To find the JDK installation directory, run:

    $ /usr/libexec/java_home

If you have multiple versions of JDK installed, you can specify a particular
version to search for with the --version flag. To find the exact version
number, run:

    $ java -version

If the version number contains a '+' symbol, replace it with '_', otherwise
Spack will think it is a variant. Add JDK as an external package by running:

    $ spack config edit packages

and adding entries for each installation:

    packages:
      jdk:
        buildable: False
        externals:
        - spec: jdk@10.0.1_10
          prefix: /path/to/jdk/Home
        - spec: jdk@1.7.0_45-b18
          prefix: /path/to/jdk/Home""".format(self.homepage)

            tty.die(msg)

    def install(self, spec, prefix):
        install_tree('.', prefix)

    def setup_run_environment(self, env):
        """Set JAVA_HOME."""

        env.set('JAVA_HOME', self.home)

    def setup_dependent_build_environment(self, env, dependent_spec):
        """Set JAVA_HOME and CLASSPATH.

        CLASSPATH contains the installation prefix for the extension and any
        other Java extensions it depends on."""

        env.set('JAVA_HOME', self.home)

        class_paths = []
        for d in dependent_spec.traverse(deptype=('build', 'run', 'test')):
            if d.package.extends(self.spec):
                class_paths.extend(find(d.prefix, '*.jar'))

        classpath = os.pathsep.join(class_paths)
        env.set('CLASSPATH', classpath)

    def setup_dependent_run_environment(self, env, dependent_spec):
        """Set CLASSPATH.

        CLASSPATH contains the installation prefix for the extension and any
        other Java extensions it depends on."""
        # For runtime environment set only the path for
        # dependent_spec and prepend it to CLASSPATH
        if dependent_spec.package.extends(self.spec):
            class_paths = find(dependent_spec.prefix, '*.jar')
            classpath = os.pathsep.join(class_paths)
            env.prepend_path('CLASSPATH', classpath)

    def setup_dependent_package(self, module, dependent_spec):
        """Allows spec['java'].home to work."""

        self.spec.home = self.home
