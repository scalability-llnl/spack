# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Vapor(CMakePackage):
    """VAPOR is the Visualization and Analysis Platform for Ocean,
    Atmosphere, and Solar Researchers. VAPOR provides an interactive 3D
    visualization environment that can also produce animations and
    still frame images.
    """

    homepage = "https://www.vapor.ucar.edu"
    url = "https://github.com/NCAR/VAPOR/archive/refs/tags/v3.9.0.tar.gz"
    git = "https://github.com/NCAR/VAPOR.git"

    maintainers("vanderwb")

    version("main", branch="main")
    version("3.9.3", sha256="0bf614ef80387f4ef313154e55861b6a36ac31cc2993f1e3899a329d272331b0")
    version("3.9.2", sha256="94b17067c707768d543888c9c3111d82a9f468290b611099889d6b6430a8e846")
    version("3.9.1", sha256="5842bfd21e8e905e1acec35e8b86bc706a5a340eeee3530e07a20debe982ca31")
    version("3.9.0", sha256="343ababe40b5824ef826f16c935a6dc1fb18e1a4c88ef967c8d64386f28a99a3")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("doc", default=True, description="Build docs using Doxygen")
    variant("ospray", default=False, description="Enable OSPRay raytracing")

    depends_on("cmake@3.17:", type="build")
    depends_on("python+ssl", type="build")
    depends_on("py-scipy", type="build")
    depends_on("py-matplotlib", type="build")
    depends_on("py-numpy@1.21", type="build")

    depends_on("zlib-api")
    depends_on("gl")

    depends_on("xz")
    depends_on("openssl")
    depends_on("expat")
    depends_on("curl")
    depends_on("mesa-glu")
    depends_on("libxtst")
    depends_on("libxcb")
    depends_on("xcb-util")
    depends_on("libxkbcommon")
    depends_on("libpng")
    depends_on("assimp")
    depends_on("netcdf-c~dap~byterange")
    depends_on("udunits")
    depends_on("freetype")
    depends_on("proj@:7")
    depends_on("libgeotiff")
    depends_on("glm")
    depends_on("qt+opengl+dbus@5")

    depends_on("ospray~mpi", when="+ospray")
    depends_on("doxygen", when="+doc")

    # These images are required but not provided by the source
    resource(
        name="map-images",
        url="https://anaconda.org/Ncar-vapor/vapor-maps-extra/1.0.0/download/noarch/vapor-maps-extra-1.0.0-0.tar.bz2",
        sha256="6d102817f13ee02d6af8842e8c20844af6fb848dcd79a42b6e24b204e9905f50",
        placement="extras",
    )

    def cmake_args(self):
        spec = self.spec
        pyvers = spec["python"].version.up_to(2)
        pypath = "{}/python{}".format(spec.prefix.lib, pyvers)

        args = [
            self.define_from_variant("BUILD_OSP", "ospray"),
            self.define_from_variant("BUILD_DOC", "doc"),
            self.define("BUILD_PYTHON", False),
            self.define("THIRD_PARTY_DIR", spec.prefix),
            self.define("THIRD_PARTY_LIB_DIR", spec.prefix.lib),
            self.define("THIRD_PARTY_INC_DIR", spec["python"].prefix.include),
            self.define("PYTHONVERSION", pyvers),
            self.define("PYTHONDIR", spec.prefix),
            self.define("PYTHONPATH", pypath),
            self.define("NUMPY_INCLUDE_DIR", pypath + "/site-packages/numpy/core/include"),
            self.define("MAP_IMAGES_PATH", "../extras/share/images"),
        ]

        return args

    # VAPOR depends on custom version of GeometryEngine that is
    # packaged with the source code - need to extract and move
    @run_before("cmake")
    def extract_gte(self):
        unzip = which("unzip")

        with working_dir("buildutils"):
            unzip("GTE.zip")
            move("GTE", "../include")

    # Build will use these optional site defaults which aren't
    # generally applicable to other sites
    @run_before("cmake")
    def clean_local_refs(self):
        force_remove("site_files/site.NCAR")

    # Vapor wants all of the Python packages in its build path. This
    # somewhat objectionable code copies packages to the tree. It also
    # copies the Python library so that the site-library is found.
    @run_before("cmake")
    def copy_python_library(self):
        spec = self.spec
        mkdirp(spec.prefix.lib)

        install_tree(spec["python"].prefix.lib, spec.prefix.lib)

        for py_dep in [dep_spec.name for dep_spec in spec.traverse()]:
            if py_dep.startswith("py-"):
                install_tree(spec[py_dep].prefix.lib, spec.prefix.lib)

    @run_before("cmake")
    def add_extra_images(self):
        install_tree("extras/share", "share")

    # The documentation will not be built without this target (though
    # it will try to install!)
    @property
    def build_targets(self):
        targets = []

        if "+doc" in self.spec:
            targets.append("doc")

        return targets + ["all"]
