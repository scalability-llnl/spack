# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.util.executable import which
from llnl.util.filesystem import join_path
import spack.config


# Class representing a resource manager command to run MPI-based code.
#
# A number of static methods are provided to help create MPIRunner's in
# different ways. Users can set parameters in config files and create a
# runner from these parameters. For example, the following section in
# config.yaml provides special params for 'mvapich2' package:
# 'mvapich2': {
#     'mpi_runner_cmd': 'mpiexec',
#     'mpi_runner_np_flags': '--npflags',
#     'mpi_runner_pre_np_flags': '--pre',
#     'mpi_runner_post_np_flags': '--post'
# }
# Users can also set parameters in a top level config section:
# 'mpi_runner_cmd': 'srun',
# 'mpi_runner_pre_np_flags': '-np'
# The static function 'create_from_conf_key' first tries the provided
# config section and then goes to the top level conf params.

class MPIRunner(object):
    """Class representing a resource manager command to run MPI-based code."""

    default_np_flags = '-n'

    def __init__(self, cmd, np_flags=default_np_flags, pre_np_flags='',
                 post_np_flags=''):
        self.cmd = cmd
        self.np_flags = np_flags
        self.pre_np_flags = pre_np_flags
        self.post_np_flags = post_np_flags

    def full_cmd(self, np=1):
        """The command-line string for the resource manager.

        Returns:
            str: The executable and default arguments
        """
        complete_cmd = '{0} {1} {2} {3} {4}'.format(
            self.cmd,
            self.pre_np_flags,
            self.np_flags,
            np,
            self.post_np_flags)
        return complete_cmd

    def full_opts(self, np=1):
        """The list of options for the resource manager.

        Returns:
            str: The executable and default arguments
        """
        opts = []
        if self.pre_np_flags != '':
            opts.extend([self.pre_np_flags])
        if self.np_flags != '':
            opts.extend([self.np_flags])
            opts.extend([str(np)])
        if self.post_np_flags != '':
            opts.extend([self.post_np_flags])
        return opts

    @staticmethod
    def create_from_conf(cfg):
        if cfg and 'mpi_runner_cmd' in cfg:
            return MPIRunner(
                cfg['mpi_runner_cmd'],
                cfg.get('mpi_runner_np_flags', MPIRunner.default_np_flags),
                cfg.get('mpi_runner_pre_np_flags', ''),
                cfg.get('mpi_runner_post_np_flags', ''))
        return None

    @staticmethod
    def create_from_conf_key(cfg_key):
        """Creates a runner from config parameters; first tries the given
        specific config key and then the top level conf.

        Returns:
            MPIRunner: runner or None if conf is not defined
        """
        runner = None
        cfg = spack.config.get('config:{0}'.format(cfg_key))  # Specific conf
        if cfg:
            runner = MPIRunner.create_from_conf(cfg)
        else:
            cfg = spack.config.get('config')  # Top level
            runner = MPIRunner.create_from_conf(cfg)

        return runner

    @staticmethod
    def create_def_runner(full_pkg_name, mpi_bindir):
        """First try specific runner config corresponding to the package name
        and then top level config; if neither is defined initialize the runner
        with 'srun' or 'mpiexec'.

        Returns:
            MPIRunner: runner or None if conf is not defined
        """
        pkg_name = full_pkg_name.split('.')[-1]
        runner = MPIRunner.create_from_conf_key(pkg_name)

        if not runner:
            return MPIRunner.query_res_manager('srun', mpi_bindir)

        return runner

    @staticmethod
    def query_res_manager(res_mgr, mpi_bindir):
        """Creates a runner for given resource manager; if resource manager
        was not found, falls back to 'mpiexec' at given directory.

        Returns:
            MPIRunner:
        """
        mgr_exe = which(res_mgr)
        if mgr_exe:
            return MPIRunner(mgr_exe.command)
        else:
            return MPIRunner(join_path(mpi_bindir, 'mpiexec'))
