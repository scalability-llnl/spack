# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import glob
import importlib
import inspect
import os
import shutil
import time

import llnl.util.filesystem as fs
import llnl.util.tty as tty

import spack.build_systems.cmake
import spack.builder
import spack.util.log_parse
from spack.builder import run_after
from spack.directives import depends_on, requires, variant
from spack.package import CMakePackage


class CTestBuilder(spack.build_systems.cmake.CMakeBuilder):
    """
    This builder mirrors the behavior of a CMakeBuilder, but all commands are run through
    CTest. This ensures that xml files are created through CTest.  This provides a unified
    buildstamp and improved xml over the spack generated ones.

    An additional phase is added for running tests post installation.  This allows for things
    like regression tests that can be used to monitior differences in behavior/performance
    without failing the install.
    """

    phases = ("cmake", "build", "install", "analysis")

    @property
    def std_cmake_args(self):
        """
        Args to always supply to CMake. CDash args don't do anything if you don't submit

        TODO: workout how to get the track,build,site mapped correctly
        Currently this ignores the spack flags, and injests the CTestConfig.cmake files

        In ExaWind it is hooked into additional infrastrucure.
        The spack flags are not ingestible to the package as far as I can currently tell.
        """
        args = super().std_cmake_args
        if self.spec.variants["cdash_submit"].value:
            args.extend(
                [
                    "-D",
                    f"BUILDNAME={self.pkg.spec.name}",
                    "-D",
                    f"CTEST_BUILD_OPTIONS={self.pkg.spec.short_spec}",
                    "-D",
                    "SITE=TODO",
                ]
            )
        return args

    def ctest_args(self):
        args = ["-T", "Test"]
        args.append("--stop-time")
        overall_test_timeout = 60 * 60 * 4  # 4 hours TODO should probably be a variant
        args.append(time.strftime("%H:%M:%S", time.localtime(time.time() + overall_test_timeout)))
        args.append("-VV")  # make sure lots of output can go to the log
        # a way to parse additional information to ctest exectution.
        # for ecample in exawind, we default to running unit-tests, but for nightly tests
        # we expand to our regression test suite through this variant
        extra_args = self.pkg.spec.variants["ctest_args"].value
        if extra_args:
            args.extend(extra_args.split())
        return args

    @property
    def build_args(self):
        """
        CTest arguments that translate to running a to the end of the build phase through CTest
        """
        args = [
            "--group",
            self.pkg.spec.name,
            "-T",
            "Start",
            "-T",
            "Configure",
            "-T",
            "Build",
            "-VV",
        ]
        return args

    @property
    def submit_args(self):
        """
        CTest arguments just for sumbmission.  Allows us to split phases, where default CTest behavior is to configure, build, test and submit from a single command.
        """
        args = ["-T", "Submit", "-V"]
        return args

    def submit_cdash(self, pkg, spec, prefix):
        ctest = Executable(self.spec["cmake"].prefix.bin.ctest)
        ctest.add_default_env("CTEST_PARALLEL_LEVEL", str(make_jobs))
        build_env = os.environ.copy()
        ctest(*self.submit_args, env=build_env)

    def build(self, pkg, spec, prefix):
        """
        The only reason to run through the CTest interface is if we want to submit to CDash with
        unified CTest xml's.
        If we aren't going to submit then we can just run as the CMakeBuilder
        """
        if self.pkg.spec.variants["cdash_submit"].value:
            ctest = Executable(self.spec["cmake"].prefix.bin.ctest)
            ctest.add_default_env("CMAKE_BUILD_PARALLEL_LEVEL", str(make_jobs))
            with fs.working_dir(self.build_directory):
                build_env = os.environ.copy()
                # have ctest run, but we still want to submit if there are build failures where spack would stop.
                # check for errors and submit to cdash if there are failures
                output = ctest(
                    *self.build_args, env=build_env, output=str.split, error=str.split
                ).split("\n")
                errors, warnings = spack.util.log_parse.parse_log_events(output)
                if len(errors) > 0:
                    errs = [str(e) for e in errors]
                    tty.warn(f"Errors: {errs}")
                    tty.warn(f"returncode {ctest.returncode}")
                    self.submit_cdash(pkg, spec, prefix)
                    raise BaseException(f"{self.pkg.spec.name} had build errors")

        else:
            super().build(pkg, spec, prefix)

    def analysis(self, pkg, spec, prefix):
        """
        This method currently runs tests post install to avoid the undesired side effect
        of failing installs for failed tests with spack's built in testing infrastructure
        """

        with working_dir(self.build_directory):
            args = self.ctest_args()
            tty.debug("{} running CTest".format(self.pkg.spec.name))
            tty.debug("Running:: ctest" + " ".join(args))
            ctest = Executable(self.spec["cmake"].prefix.bin.ctest)
            ctest.add_default_env("CTEST_PARALLEL_LEVEL", str(make_jobs))
            ctest.add_default_env("CMAKE_BUILD_PARALLEL_LEVEL", str(make_jobs))
            build_env = os.environ.copy()
            ctest(*args, "-j", str(make_jobs), env=build_env, fail_on_error=False)

            if self.pkg.spec.variants["cdash_submit"].value:
                self.submit_cdash(pkg, spec, prefix)


class CtestPackage(CMakePackage):
    """
    This package's default behavior is to act as a Standard CMakePackage,
    """

    CMakeBuilder = CTestBuilder
    variant("cdash_submit", default=False, description="Submit results to cdash")
    variant("ctest_args", default="", description="quoted string of arguments to send to ctest")

    def setup_build_environment(self, env):
        env.prepend_path("PYTHONPATH", os.environ["EXAWIND_MANAGER"])

    def do_clean(self):
        """
        A nice feature for development builds.  Can be omitted from the final product.
        """
        super().do_clean()
        if not self.stage.managed_by_spack:
            build_artifacts = glob.glob(os.path.join(self.stage.source_path, "spack-*"))
            for f in build_artifacts:
                if os.path.isfile(f):
                    os.remove(f)
                if os.path.isdir(f):
                    shutil.rmtree(f)
            ccjson = os.path.join(self.stage.source_path, "compile_commands.json")

            if os.path.isfile(ccjson):
                os.remove(ccjson)

    @run_after("cmake")
    def copy_compile_commands(self):
        """
        A nice feature for development builds.  Can be omitted from the final product.
        """
        if self.spec.satisfies("dev_path=*"):
            target = os.path.join(self.stage.source_path, "compile_commands.json")
            source = os.path.join(self.build_directory, "compile_commands.json")
            if os.path.isfile(source):
                shutil.copyfile(source, target)
