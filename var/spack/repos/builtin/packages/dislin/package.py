# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dislin(Package):
    """DISLIN is a high level and easy to use graphics library for displaying
    data as curves,  bar graphs,  pie charts,  3D-colour plots,  surfaces,
    contours and maps."""

    homepage = "https://www.mps.mpg.de/dislin"
    url = "ftp://ftp.gwdg.de/pub/grafik/dislin/linux/i586_64/dislin-11.0.linux.i586_64.tar.gz"

    version("11.0", sha256="13d28188924e0b0b803d72aa4b48be4067e98e890701b0aa6f54a11c7d34dd10")

    depends_on("motif")
    depends_on("gl")
    depends_on("glx")

    @property
    def libs(self):
        query_parameters = self.spec.last_query.extra_parameters
        query2libraries = {
            tuple(): ["libdislin"],
            ("d",): ["libdislin_d"],
            ("c",): ["libdislnc"],
            ("cd",): ["libdislnc_d"],
            ("cxx",): ["libdiscpp"],
            ("java",): ["libdisjava"],
        }

        key = tuple(query_parameters)
        libraries = query2libraries[key]

        return find_libraries(libraries, root=self.prefix, shared=True, recursive=True)

    def setup_build_environment(self, env):
        env.set("DISLIN", self.prefix)

    def setup_run_environment(self, env):
        env.set("DISLIN", self.prefix)
        env.prepend_path("PATH", self.prefix)
        env.prepend_path("LD_LIBRARY_PATH", self.prefix)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["motif"].prefix.lib)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["mesa"].prefix.lib)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path("LD_LIBRARY_PATH", self.prefix)

    def install(self, spec, prefix):
        install = Executable("./INSTALL")
        install()
        with working_dir("examples"):
            install("dislin_d.h", prefix)
