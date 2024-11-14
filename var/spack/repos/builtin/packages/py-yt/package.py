# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyYt(PythonPackage):
    """Volumetric Data Analysis

    yt is a python package for analyzing and visualizing
    volumetric, multi-resolution data from astrophysical
    simulations, radio telescopes, and a burgeoning
    interdisciplinary community.
    """

    homepage = "https://yt-project.org"
    git = "https://github.com/yt-project/yt.git"
    pypi = "yt/yt-4.1.2.tar.gz"

    maintainers("charmoniumq")

    license("BSD-3-Clause")

    version("4.4.0", sha256="0e15df9cb21abe582f8128bf0705a3bc0f4805f97efd6b4f883073703941c0d5")
    version("4.1.2", sha256="0ae03288b067721baad14c016f253dc791cd444a1f2dd5d804cf91da622a0c76")
    version("3.6.1", sha256="be454f9d05dcbe0623328b4df43a1bfd1f0925e516be97399710452931a19bb0")
    version("3.6.0", sha256="effb00536f19fd2bdc18f67dacd5550b82066a6adce5b928f27a01d7505109ec")
    version("3.5.1", sha256="c8ef8eceb934dc189d63dc336109fad3002140a9a32b19f38d1812d5d5a30d71")
    version("3.5.0", sha256="ee4bf8349f02ce21f571654c26d85c1f69d9678fc8f5c7cfe5d1686c7ed2e3ca")
    version("3.4.1", sha256="a4cfc47fe21683e7a3b680c05fe2a25fb774ffda6e3939a35755e5bf64065895")
    version("3.4.0", sha256="de52057d1677473a83961d8a1119a9beae3121ec69a4a5469c65348a75096d4c")
    version("3.3.5", sha256="4d5c751b81b0daf6dcaff6ec0faefd97138c008019b52c043ab93403d71cedf6")
    version("3.3.4", sha256="64c109ba4baf5afc0e1bc276ed2e3de13f1c5ce85c6d8b4c60e9a47c54bf3bcb")
    version("3.3.3", sha256="edf6453927eee311d4b51afacb52cd5504b2b57cc6d3d92dab9c6bfaf6d883df")
    version("3.3.2", sha256="a18e4cf498349804c64eec6509ec4d3a6beaa34ea63366543290c35774337f0e")
    version("3.3.1", sha256="01e3b3398d43b8eab698d55ba37ef3d701ea026b899c0940a1ee34b215e25a31")
    version("3.3.0", sha256="537c67e85c8f5cc5530a1223a74d27eb7f11c459651903c3092c6a97b450d019")
    version("3.2.3", sha256="4d6ccf345d9fab965335c9faf8708c7eea79366b81d77f0f302808be3e82c0ed")
    version("3.2.2", sha256="78866f51e4751534ad60987000f149a8295952b99b37ca249d45e4d11095a5df")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    variant("astropy", default=True, description="enable astropy support")
    variant("h5py", default=True, description="enable h5py support")
    variant("scipy", default=True, description="enable scipy support")
    variant("rockstar", default=False, description="enable rockstar support")

    with when("@4.4.0:"):
        # Build dependencies:
        depends_on("py-setuptools@61.2:", type="build")
        depends_on("py-cython@3.0.3:", type="build")
        depends_on("py-numpy@2.0.0:", type="build")
        depends_on("py-ewah-bool-utils@1.2.0:", type=("build", "run"))

        # Main dependencies:
        depends_on("py-cmyt@1.1.2:", type=("build", "run"))
        depends_on("py-matplotlib@3.5:", type=("build", "run"))
        depends_on("py-numpy@1.21:2", type=("build", "run"))
        conflicts("^py-numpy@2.0.1", when="target=aarch64 platform=darwin")
        depends_on("py-pillow@8.3.2:", type=("build", "run"))
        depends_on("py-unyt@2.9.2:", type=("build", "run"))
        depends_on("py-typing-extensions@4.4.0:", type=("build", "run"), when="^python@:3.11")

        depends_on("py-h5py@3.1.0:", type=("build", "run"), when="+h5py")
        conflicts("^py-h5py@3.12.0", when="platform=windows")

        depends_on("py-netcdf4@1.5.3:", type=("build", "run"), when="+netCDF4")
        conflicts("^py-netcdf4@1.6.1", when="+netCDF4")

        depends_on("py-f90nml@1.1:", type=("build", "run"), when="+Fortran")
        depends_on("py-astropy@4.0.1:", type=("build", "run"), when="+astropy")

        # Extras:
        variant("netCDF4", default=False, description="enable netCDF4 support")
        variant("Fortran", default=False, description="enable Fortran support")

        variant("adaptahop", default=False, description="enable adaptahop support (no-op)")
        variant("ahf", default=False, description="enable ahf support (no-op)")
        variant("amrex", default=False, description="enable amrex support (no-op)")
        variant("amrvac", default=False, description="enable amrvac support")
        variant("art", default=False, description="enable art support (no-op)")
        variant("arepo", default=False, description="enable arepo support")
        variant("artio", default=False, description="enable artio support (no-op)")
        variant("athena", default=False, description="enable athena support (no-op)")
        variant("athena_pp", default=False, description="enable athena-pp support (no-op)")
        variant("boxlib", default=False, description="enable boxlib support (no-op)")
        # variant("cf_radial", default=False, description="enable cf-radial support")
        variant("chimera", default=False, description="enable chimera support")
        variant("chombo", default=False, description="enable chombo support")
        variant("cholla", default=False, description="enable cholla support")
        variant("eagle", default=False, description="enable eagle support")
        variant("enzo_e", default=False, description="enable enzo-e support")
        variant("enzo", default=False, description="enable enzo support")
        variant("exodus_ii", default=False, description="enable exodus-ii support")
        variant("fits", default=False, description="enable fits support")
        variant("flash", default=False, description="enable flash support")
        variant("gadget", default=False, description="enable gadget support")
        variant("gadget_fof", default=False, description="enable gadget-fof support")
        variant("gamer", default=False, description="enable gamer support")
        variant("gdf", default=False, description="enable gdf support")
        variant("gizmo", default=False, description="enable gizmo support")
        variant("halo_catalog", default=False, description="enable halo-catalog support")
        variant("http_stream", default=False, description="enable http-stream support")
        variant("idefix", default=False, description="enable idefix support")
        variant("moab", default=False, description="enable moab support")
        variant("nc4_cm1", default=False, description="enable nc4-cm1 support")
        variant("open_pmd", default=False, description="enable open-pmd support")
        variant("owls", default=False, description="enable owls support")
        variant("owls_subfind", default=False, description="enable owls-subfind support")
        variant("parthenon", default=False, description="enable parthenon support")
        variant("ramses", default=False, description="enable ramses support")
        variant("sdf", default=False, description="enable sdf support")
        variant("stream", default=False, description="enable stream support (no-op)")
        variant("swift", default=False, description="enable swift support")
        variant("tipsy", default=False, description="enable tipsy support (no-op)")
        variant("ytdata", default=False, description="enable ytdata support")

        conflicts("~Fortran", when="+amrvac")

        conflicts("~h5py", when="+arepo")
        # depends_on("py-xarray@0.16.1:", when="+cf_radial", type=('build', 'run'))
        # depends_on("py-arm-pyart@1.19.2:", when="+cf_radial", type=('build', 'run'))
        conflicts("~h5py", when="+chimera")
        conflicts("~h5py", when="+chombo")
        conflicts("~h5py", when="+cholla")
        conflicts("~h5py", when="+eagle")
        conflicts("~h5py", when="+enzo_e")
        depends_on("py-libconf@1.0.1:", when="+enzo_e", type=("build", "run"))
        conflicts("~h5py", when="+enzo")
        depends_on("py-libconf@1.0.1:", when="+enzo", type=("build", "run"))
        conflicts("~netCDF4", when="+exodus_ii")
        depends_on("py-astropy@4.0.1:", when="+fits", type=("build", "run"))
        depends_on("py-regions@0.7:", when="+fits", type=("build", "run"))
        conflicts("~h5py", when="+flash")
        conflicts("~h5py", when="+gadget")
        conflicts("~h5py", when="+gadget_fof")
        conflicts("~h5py", when="+gamer")
        conflicts("~h5py", when="+gdf")
        conflicts("~h5py", when="+gizmo")
        conflicts("~h5py", when="+halo_catalog")
        depends_on("py-requests@2.20.0:", when="+http_stream", type=("build", "run"))
        conflicts("~h5py", when="+idefix")
        conflicts("~h5py", when="+moab")
        conflicts("~netCDF4", when="+nc4_cm1")
        conflicts("~h5py", when="+open_pmd")
        conflicts("~h5py", when="+owls")
        conflicts("~h5py", when="+owls_subfind")
        conflicts("~h5py", when="+parthenon")
        conflicts("~Fortran", when="+ramses")
        depends_on("py-scipy", when="+ramses", type=("build", "run"))
        depends_on("py-requests@2.20.0:", when="+sdf", type=("build", "run"))
        conflicts("~h5py", when="+swift")
        conflicts("~h5py", when="+ytdata")

        # variant('full', default=False, description='Enable all optional dependencies')

    # Main dependencies:
    # See https://github.com/yt-project/yt/blob/yt-4.1.2/setup.cfg#L40
    depends_on("py-cmyt@0.2.2:", type=("build", "run"), when="@4.1.2:")
    depends_on("py-ipywidgets@8:", type=("build", "run"), when="@4.1.2")
    depends_on("py-matplotlib@1.5.3:", type=("build", "run"))
    depends_on("py-matplotlib@:3.2.2", type=("build", "run"), when="@:3.6.0")
    depends_on("py-matplotlib@3.1:", type=("build", "run"), when="@4.1.2:")
    conflicts("^py-matplotlib@3.4.2", when="@4.1.2:")
    depends_on("py-more-itertools@8.4:", type=("build", "run"), when="@4.1.2:")
    depends_on("py-numpy@1.10.4:", type=("build", "run"))
    depends_on("py-numpy@1.14.5:", type=("build", "run"), when="@4.1.2:")
    # https://github.com/yt-project/yt/pull/4859
    depends_on("py-numpy@:1", when="@:4.3.0", type=("build", "run"))
    depends_on("py-packaging@20.9:", type=("build", "run"), when="@4.1.2:")
    # PIL/pillow and pyparsing dependency is handled by matplotlib
    depends_on("py-tomli-w@0.4:", type=("build", "run"), when="@4.1.2:")
    depends_on("py-tqdm@3.4.0:", type=("build", "run"), when="@4.1.2:")
    depends_on("py-unyt@2.8:2", type=("build", "run"), when="@4.1.2")
    depends_on("py-importlib-metadata@1.4:", type=("build", "run"), when="@4.1.2: ^python@:3.7")
    depends_on("py-tomli@1.2.3:", type=("build", "run"), when="@4.1.2: ^python@:3.10")
    depends_on("py-typing-extensions@4.2:", type=("build", "run"), when="@4.1.2: ^python@:3.7")
    # See https://github.com/spack/spack/pull/30418#discussion_r863962805
    depends_on("py-ipython@1.0:", type=("build", "run"), when="@:3")

    # Extras:
    # See https://github.com/yt-project/yt/blob/yt-4.1.2/setup.cfg#L80
    depends_on("py-h5py@3.1:3", type=("build", "run"), when="@:4.1.2 +h5py")
    depends_on("py-scipy@1.5.0:", type=("build", "run"), when="+scipy")
    depends_on("rockstar@yt", type=("build", "run"), when="+rockstar")
    depends_on("py-astropy@4.0.1:5", type=("build", "run"), when="@:4.1.2 +astropy")

    # Build dependencies:
    # See https://github.com/yt-project/yt/blob/yt-4.1.2/pyproject.toml#L2
    depends_on("py-cython@0.24:", type="build")
    depends_on("py-cython@0.29.21:2", type="build", when="@4.1.2")
    depends_on("py-wheel@0.36.2:", type="build", when="@4.1.2:")
    depends_on("py-setuptools@19.6:", type=("build", "run"))
    depends_on("py-setuptools@59.0.1:", type=("build", "run"), when="@4.1.2:")

    @run_before("install")
    def prep_yt(self):
        if "+rockstar" in self.spec:
            with open("rockstar.cfg", "w") as rockstar_cfg:
                rockstar_cfg.write(self.spec["rockstar"].prefix)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        # The Python interpreter path can be too long for this
        # yt = Executable(join_path(prefix.bin, "yt"))
        # yt("--help")
        python(join_path(self.prefix.bin, "yt"), "--help")

    def setup_build_environment(self, env):
        env.set("MAX_BUILD_CORES", str(make_jobs))
