##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
#
# Author: Justin Too <too1@llnl.gov>
#
import distutils.dir_util
from spack import *


class Jdk(Package):
    """The Java Development Kit (JDK) released by Oracle Corporation
       in the form of a binary product aimed at Java developers."""
    homepage = "http://www.oracle.com/technetwork/java/javase/downloads/index.html"

    # Oracle requires that you accept their License Agreement in order
    # to access the Java packages in download.oracle.com. In order to
    # automate this process, we need to utilize these additional curl
    # commandline options.
    #
    # See http://stackoverflow.com/questions/10268583/how-to-automate-download-and-installation-of-java-jdk-on-linux
    cookies = {'oraclelicense': 'accept-securebackup-cookie'}

    # For instructions on how to find the magic URL, see:
    # https://gist.github.com/P7h/9741922
    # https://linuxconfig.org/how-to-install-java-se-development-kit-on-debian-linux
    version('8u172-b11', 'eda2945e8c02b84adbf78f46c37b71c1', cookies=cookies,
            url='http://download.oracle.com/otn-pub/java/jdk/8u172-b11/a58eab1ec242421181065cdc37240b08/jdk-8u172-linux-x64.tar.gz')
    version('8u141-b15', '8cf4c4e00744bfafc023d770cb65328c', cookies=cookies,
            url='http://download.oracle.com/otn-pub/java/jdk/8u141-b15/336fa29ff2bb4ef291e347e091f7f4a7/jdk-8u141-linux-x64.tar.gz')
    version('8u131-b11', '75b2cb2249710d822a60f83e28860053', cookies=cookies,
            url='http://download.oracle.com/otn-pub/java/jdk/8u131-b11/d54c1d3a095b4ff2b6607d096fa80163/jdk-8u131-linux-x64.tar.gz')
    version('8u92-b14',  '65a1cc17ea362453a6e0eb4f13be76e4', cookies=cookies)
    version('8u73-b02',  '1b0120970aa8bc182606a16bf848a686', cookies=cookies)
    version('8u66-b17',  '88f31f3d642c3287134297b8c10e61bf', cookies=cookies)
    # The 7u80 tarball is not readily available from Oracle.  If you have
    # the tarball, add it to your mirror as mirror/jdk/jdk-7u80.tar.gz and
    # away you go.
    version('7u80-b0', '6152f8a7561acf795ca4701daa10a965')

    provides('java@8', when='@8u0:8u999')
    provides('java@7', when='@7u0:7u999')

    def url_for_version(self, version):
        url = "http://download.oracle.com/otn-pub/java/jdk/{0}/jdk-{1}-linux-x64.tar.gz"
        version = str(version)
        minor_version = version[:version.index('-')]
        return url.format(version, minor_version)

    def install(self, spec, prefix):
        distutils.dir_util.copy_tree(".", prefix)

    def setup_environment(self, spack_env, run_env):
        run_env.set('JAVA_HOME', self.spec.prefix)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('JAVA_HOME', self.spec.prefix)
