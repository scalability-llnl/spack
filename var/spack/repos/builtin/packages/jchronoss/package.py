# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Jchronoss(CMakePackage):
    """ JCHRONOSS aims to help HPC application testing process
     to scale as much as the application does. """

    homepage = "http://jchronoss.hpcframework.com"
    url      = "http://fs.paratools.com/mpc/contrib/apps/jchronoss/JCHRONOSS-1.2.tar.gz"

    version('1.2',   sha256='52a565a28c0b83b433065060863d29f2b3e4b05f4f26b7a5893a21a2c66d6eba')
    version('1.1.1', sha256='5a11463b7295817f503c58dda1a82c0d3568bdee5e9d13d59e00d337ba84dc45')
    version('1.1',   sha256='e8230416c94fb58516a4b9293efd0a67edf4a37e82cfae2ced2c0af8b4615f22')
    version('1.0',   sha256='6a92d3cf2424fc7eaaeac9bfefe395596275e552ac5660eb4543e43679586f24')

    variant("realtime", default=False, description="Enable Real-Time support")
    variant("openmp", default=False, description="Enable OpenMP constructs")
    variant("ncurses", default=False, description="Enable ncurses-based tool")
    variant('color', default=False, description='Enable colour-themed output')

    depends_on("libxml2")
    depends_on("libwebsockets", when="+realtime")
    depends_on("libev", when="+realtime")
    depends_on("ncurses", when="+ncurses")

    def cmake_args(self):
        args = ["-DSPACK_DRIVEN=ON"]

        if '+color' in self.spec:
            args.append("-DENABLE_COLOR=yes")
        if '+openmp' in self.spec:
            args.append("-DENABLE_OPENMP=yes")
        if '+ncurses' in self.spec:
            args.append("-DENABLE_PLUGIN_NCURSES=yes")
        if '+realtime' in self.spec:
            args.append("-DENABLE_PLUGIN_SERVER=yes")

        return args
