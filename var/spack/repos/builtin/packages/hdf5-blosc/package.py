# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil
import sys

from spack.package import *


def _install_shlib(name, src, dst):
    """Install a shared library from directory src to directory dst"""
    if sys.platform == "darwin":
        shlib0 = name + ".0.dylib"
        shlib = name + ".dylib"
        install(join_path(src, shlib0), join_path(dst, shlib0))
        os.symlink(shlib0, join_path(dst, shlib))
    else:
        shlib000 = name + ".so.0.0.0"
        shlib0 = name + ".so.0"
        shlib = name + ".dylib"
        install(join_path(src, shlib000), join_path(dst, shlib000))
        os.symlink(shlib000, join_path(dst, shlib0))
        os.symlink(shlib0, join_path(dst, shlib))


class Hdf5Blosc(Package):
    """Blosc filter for HDF5"""

    homepage = "https://github.com/Blosc/hdf5-blosc"
    git = "https://github.com/Blosc/hdf5-blosc.git"

    license("MIT")

    version("master", branch="master")

    depends_on("c", type="build")  # generated

    depends_on("c-blosc")
    depends_on("hdf5")
    depends_on("libtool", type="build")

    parallel = False

    def install(self, spec, prefix):
        # The included cmake recipe doesn"t work for Darwin
        # cmake(".", *std_cmake_args)
        #
        # make()
        # make("install")
        # if sys.platform == "darwin":
        #     fix_darwin_install_name(prefix.lib)

        libtool = spec["libtool"].command

        # TODO: these vars are not used.
        # if "+mpi" in spec["hdf5"]:
        #     cc = "mpicc"
        # else:
        #     cc = "cc"
        # shlibext = "so" if sys.platform != "darwin" else "dylib"

        mkdirp(prefix.include)
        mkdirp(prefix.lib)

        # Build and install filter
        with working_dir("src"):
            libtool("--mode=compile", "--tag=CC", "cc", "-g", "-O", "-c", "blosc_filter.c")
            libtool(
                "--mode=link",
                "--tag=CC",
                "cc",
                "-g",
                "-O",
                "-rpath",
                prefix.lib,
                "-o",
                "libblosc_filter.la",
                "blosc_filter.lo",
                "-L%s" % spec["c-blosc"].prefix.lib,
                "-lblosc",
                "-L%s" % spec["hdf5"].prefix.lib,
                "-lhdf5",
            )
            _install_shlib("libblosc_filter", ".libs", prefix.lib)

            # Build and install plugin
            # The plugin requires at least HDF5 1.8.11:
            if spec["hdf5"].satisfies("@1.8.11:"):
                libtool("--mode=compile", "--tag=CC", "cc", "-g", "-O", "-c", "blosc_plugin.c")
                libtool(
                    "--mode=link",
                    "--tag=CC",
                    "cc",
                    "-g",
                    "-O",
                    "-rpath",
                    prefix.lib,
                    "-o",
                    "libblosc_plugin.la",
                    "blosc_plugin.lo",
                    "-L%s" % prefix.lib,
                    "-lblosc_filter",
                    "-L%s" % spec["c-blosc"].prefix.lib,
                    "-lblosc",
                    "-L%s" % spec["hdf5"].prefix.lib,
                    "-lhdf5",
                )
                _install_shlib("libblosc_plugin", ".libs", prefix.lib)

        if self.run_tests:
            self.check_install(spec)

    def check_install(self, spec):
        "Build and run a small program to test the installed HDF5 Blosc plugin"
        print("Checking HDF5-Blosc plugin...")
        checkdir = "spack-check"
        with working_dir(checkdir, create=True):
            source = r"""\
#include <hdf5.h>
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#define FILTER_BLOSC 32001 /* Blosc filter ID registered with the HDF group */

int main(int argc, char **argv) {
  herr_t herr;
  hid_t file = H5Fcreate("file.h5", H5F_ACC_TRUNC, H5P_DEFAULT, H5P_DEFAULT);
  assert(file >= 0);
  hsize_t dims[3] = {10, 10, 10};
  hid_t space = H5Screate_simple(3, dims, NULL);
  assert(space >= 0);
  hid_t create_proplist = H5Pcreate(H5P_DATASET_CREATE);
  assert(create_proplist >= 0);
  herr = H5Pset_chunk(create_proplist, 3, dims);
  assert(herr >= 0);
  herr = H5Pset_filter(create_proplist, FILTER_BLOSC, H5Z_FLAG_OPTIONAL, 0,
                       NULL);
  assert(herr >= 0);
  htri_t all_filters_avail = H5Pall_filters_avail(create_proplist);
  assert(all_filters_avail > 0);
  hid_t dataset = H5Dcreate(file, "dataset", H5T_NATIVE_DOUBLE, space,
                            H5P_DEFAULT, create_proplist, H5P_DEFAULT);
  assert(dataset >= 0);
  double data[10][10][10];
  for (int k=0; k<10; ++k) {
    for (int j=0; j<10; ++j) {
      for (int i=0; i<10; ++i) {
        data[k][j][i] = 1.0 / (1.0 + i + j + k);
      }
    }
  }
  herr = H5Dwrite(dataset, H5T_NATIVE_DOUBLE, space, space, H5P_DEFAULT,
                  &data[0][0][0]);
  assert(herr >= 0);
  herr = H5Pclose(create_proplist);
  assert(herr >= 0);
  herr = H5Dclose(dataset);
  assert(herr >= 0);
  herr = H5Sclose(space);
  assert(herr >= 0);
  herr = H5Fclose(file);
  assert(herr >= 0);
  printf("Done.\n");
  return 0;
}
"""
            expected = """\
Done.
"""
            with open("check.c", "w") as f:
                f.write(source)
            if "+mpi" in spec["hdf5"]:
                cc = Executable(spec["mpi"].mpicc)
            else:
                cc = Executable(self.compiler.cc)
            # TODO: Automate these path and library settings
            cc("-c", "-I%s" % spec["hdf5"].prefix.include, "check.c")
            cc("-o", "check", "check.o", "-L%s" % spec["hdf5"].prefix.lib, "-lhdf5")
            try:
                check = Executable("./check")
                output = check(output=str)
            except ProcessError:
                output = ""
            success = output == expected
            if not success:
                print("Produced output does not match expected output.")
                print("Expected output:")
                print("-" * 80)
                print(expected)
                print("-" * 80)
                print("Produced output:")
                print("-" * 80)
                print(output)
                print("-" * 80)
                print("Environment:")
                env = which("env")
                env()
                raise RuntimeError("HDF5 Blosc plugin check failed")
        shutil.rmtree(checkdir)

    def setup_build_environment(self, env):
        env.append_path("HDF5_PLUGIN_PATH", self.spec.prefix.lib)

    def setup_run_environment(self, env):
        env.append_path("HDF5_PLUGIN_PATH", self.spec.prefix.lib)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.append_path("HDF5_PLUGIN_PATH", self.spec.prefix.lib)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.append_path("HDF5_PLUGIN_PATH", self.spec.prefix.lib)
