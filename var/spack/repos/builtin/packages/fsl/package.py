# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.package import *
from spack.util.environment import EnvironmentModifications


class Fsl(Package, CudaPackage):
    """FSL is a comprehensive library of analysis tools for FMRI, MRI and DTI
    brain imaging data."""

    # NOTE: A manual download is required for FSL.  Spack will search your
    # current directory for the download file.  Alternatively, add this file to
    # a mirror so that Spack can find it.  For instructions on how to set up a
    # mirror, see https://spack.readthedocs.io/en/latest/mirrors.html

    homepage = "https://fsl.fmrib.ox.ac.uk"
    url = "file://{0}/fsl-5.0.10-sources.tar.gz".format(os.getcwd())
    manual_download = True

    version("6.0.5", sha256="df12b0b1161a26470ddf04e4c5d5d81580a04493890226207667ed8fd2b4b83f")
    version("6.0.4", sha256="58b88f38e080b05d70724d57342f58e1baf56e2bd3b98506a72b4446cad5033e")
    version("5.0.10", sha256="ca183e489320de0e502a7ba63230a7f55098917a519e8c738b005d526e700842")

    depends_on("python", type=("build", "run"))
    depends_on("expat")
    depends_on("libx11")
    depends_on("glu")
    depends_on("iconv")
    depends_on("openblas", when="@6:")
    depends_on("vtk@:8")

    conflicts("cuda_arch=none", when="+cuda", msg="must select a CUDA architecture")
    conflicts("platform=darwin", msg="currently only packaged for linux")

    patch("build_log.patch")
    patch("eddy_Makefile.patch", when="@6.0.4")
    patch("iconv.patch", when="^libiconv")
    patch("fslpython_install_v5.patch", when="@:5")
    patch("fslpython_install_v604.patch", when="@6.0.4")
    patch("fslpython_install_v605.patch", when="@6.0.5")

    # Allow fsl to use newer versions of cuda
    patch(
        "https://aur.archlinux.org/cgit/aur.git/plain/005-fix_cuda_thrust_include.patch?h=fsl",
        sha256="9471addfc2f880350eedadcb99cb8b350abf42be1c0652ccddf49e34e5e48734",
        level=2,
    )

    # allow newer compilers
    patch("libxmlpp_bool.patch")

    # These patches disable FSL's attempts to try to submit a subset of FSL
    # computations to an SGE queue system. That auto-submit mechanism only
    # works for SGE and requires someone to edit the fsl_sub script to
    # accommodate their system. These patches disable the auto submission
    # scheme and allow the fsl_sub script to behave the same on all systems,
    # and without further modification, whether the computation is submitted to
    # a "local" system, like a workstation, or as a batch job to a cluster
    # queueing system, regardless of queue system type.
    patch("fsl_sub_v5.patch", when="@:5")
    patch("fsl_sub_v6.patch", when="@6:")

    def patch(self):
        # Uncomment lines in source file to allow building from source
        with working_dir(join_path(self.stage.source_path, "etc", "fslconf")):
            sourced = FileFilter("fsl.sh")
            sourced.filter("#FSLCONFDIR", "FSLCONFDIR")

            if self.spec.satisfies("@6:"):
                sourced.filter("#FSLMACHTYPE", "FSLMACHTYPE")
            else:
                sourced.filter(r"#(FSLMACHTYPE).*", r"\1=linux_64-gcc4.8")

        if self.spec.satisfies("@:5"):
            with working_dir(join_path(self.stage.source_path, "config", "common")):
                buildproj = FileFilter("buildproj")
                buildproj.filter(r"(^FSLMACHTYPE).*", r"\1=linux_64-gcc4.8")

        # Capture the settings file
        if self.spec.satisfies("@6:"):
            settings_file = join_path(self.stage.source_path, "config", "buildSettings.mk")
            vtk_file = settings_file
        else:
            settings_file = join_path(
                self.stage.source_path, "config", "linux_64-gcc4.8", "systemvars.mk"
            )
            externals_file = join_path(
                self.stage.source_path, "config", "linux_64-gcc4.8", "externallibs.mk"
            )
            vtk_file = externals_file

        build_settings = FileFilter(settings_file)
        vtk_settings = FileFilter(vtk_file)

        build_settings.filter(r"^CUDAVER", "#CUDAVER")
        build_settings.filter(r"(^CC)\s*=.*", r"\1 = {0}".format(spack_cc))
        build_settings.filter(r"(^CXX)\s*=.*", r"\1 = {0}".format(spack_cxx))
        build_settings.filter(r"(^CXX11)\s*=.*", r"\1 = {0}".format(spack_cxx))

        vtk_suffix = self.spec["vtk"].version.up_to(2)
        vtk_lib_dir = self.spec["vtk"].prefix.lib64
        vtk_include_dir = join_path(self.spec["vtk"].prefix.include, "vtk-{0}".format(vtk_suffix))

        vtk_settings.filter(r"(^VTKDIR_INC)\s*=.*", r"\1 = {0}".format(vtk_include_dir))
        vtk_settings.filter(r"(^VTKDIR_LIB)\s*=.*", r"\1 = {0}".format(vtk_lib_dir))
        vtk_settings.filter(r"(^VTKSUFFIX)\s*=.*", r"\1 = -{0}".format(vtk_suffix))

        if self.spec.satisfies("+cuda"):
            cuda_arch = self.spec.variants["cuda_arch"].value
            cuda_gencode = " ".join(self.cuda_flags(cuda_arch))
            cuda_installation = self.spec["cuda"].prefix

            build_settings.filter(
                r"(^CUDA_INSTALLATION)\s*=.*", r"\1 = {0}".format(cuda_installation)
            )
            build_settings.filter(
                r"(^LIB_CUDA)\s*=.*", r"\1 = {0}".format(join_path(cuda_installation, "lib64"))
            )
            build_settings.filter(
                r"(^INC_CUDA)\s*=.*", r"\1 = {0}".format(join_path(cuda_installation, "include"))
            )
            build_settings.filter(
                r"(^NVCC11)\s*=.*", r"\1 = {0}".format(join_path(cuda_installation, "bin", "nvcc"))
            )
            build_settings.filter(
                r"(^NVCC)\s*=.*", r"\1 = {0}".format(join_path(cuda_installation, "bin", "nvcc"))
            )
            build_settings.filter(r"(^GENCODE_FLAGS)\s*=.*", r"\1 = {0}".format(cuda_gencode))

            if self.spec.satisfies("@6:"):
                build_settings.filter(r"(^EDDYBUILDPARAMETERS)\s*=.*", r'\1 = "cuda=1" "cpu=1"')
                build_settings.filter(r"(^fdt_MASTERBUILD)\s*=.*", r"\1 = COMPILE_GPU=1")
                build_settings.filter(r"(^ptx2_MASTERBUILD)\s*=.*", r"\1 = COMPILE_GPU=1")
            else:
                with open(settings_file, "a") as f:
                    f.write("COMPILE_GPU=1\n")
        else:
            build_settings.filter(r"^CUDA_INSTALLATION", "#CUDA_INSTALLATION")
            build_settings.filter(r"^GENCODE_FLAGS", "#GENCODE_FLAGS")
            build_settings.filter(r"^LIB_CUDA", "#LIB_CUDA")
            build_settings.filter(r"^INC_CUDA", "#INC_CUDA")
            build_settings.filter(r"^NVCC", "#NVCC")

            if self.spec.satisfies("@6:"):
                build_settings.filter(r"(^EDDYBUILDPARAMETERS)\s*=.*", r'\1 = "cpu=1"')
                build_settings.filter(r"(^fdt_MASTERBUILD)\s*=.*", r"\1 = COMPILE_GPU=0")
                build_settings.filter(r"(^ptx2_MASTERBUILD)\s*=.*", r"\1 = COMPILE_GPU=0")

        filter_file(
            r'(configure_opts=".*)"',
            r'\1 --x-includes={0} --x-libraries={1}"'.format(
                self.spec["libx11"].prefix.include, self.spec["libx11"].prefix.lib
            ),
            join_path("extras", "src", "tk", "unix", "fslconfigure"),
        )
        filter_file(r" -L/lib64", r"", join_path("src", "fabber_core", "Makefile"))

    def install(self, spec, prefix):
        build = Executable(join_path(self.stage.source_path, "build"))
        build()

        rm = which("rm")
        for file in glob.glob("build*"):
            rm("-f", file)
        rm("-r", "-f", "src")
        rm("-r", "-f", join_path("extras", "src"))
        rm("-r", "-f", join_path("extras", "include"))

        install_tree(".", prefix)

    @run_after("install")
    def postinstall(self):
        # The PYTHON  related environment variables need to be unset here so
        # the post install script does not get confused.
        vars_to_unset = ["PYTHONPATH", "PYTHONHOME"]

        with spack.util.environment.preserve_environment(*vars_to_unset):
            for v in vars_to_unset:
                del os.environ[v]

            script = Executable(join_path(prefix, "etc", "fslconf", "post_install.sh"))
            script("-f", prefix)

    def setup_build_environment(self, env):
        if not self.stage.source_path:
            self.stage.fetch()
            self.stage.expand_archive()

        env.set("FSLDIR", self.stage.source_path)

        # Below is for sourcing purposes during building
        fslsetup = join_path(self.stage.source_path, "etc", "fslconf", "fsl.sh")

        if os.path.isfile(fslsetup):
            env.extend(EnvironmentModifications.from_sourcing_file(fslsetup))

    def setup_run_environment(self, env):
        # Set the environment variables after copying tree
        env.set("FSLDIR", self.prefix)
        fslsetup = join_path(self.prefix, "etc", "fslconf", "fsl.sh")

        if os.path.isfile(fslsetup):
            env.extend(EnvironmentModifications.from_sourcing_file(fslsetup))
