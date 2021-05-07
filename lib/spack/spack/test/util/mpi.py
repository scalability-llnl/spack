# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.filesystem as fs
from spack.util.mpi import MPIRunner
import spack.config


runner_conf_specific = {
    'mpirunner_cfg': {
        'mpi_runner_cmd': 'srun',
        'mpi_runner_np_flags': '--sflags',
        'mpi_runner_pre_np_flags': '--pre',
        'mpi_runner_post_np_flags': '--post'
    }
}

runner_conf_general = {
    'mpi_runner_cmd': 'mpirunrun',
    'mpi_runner_pre_np_flags': '-p'
}


def test_mpirunner(tmpdir):
    with spack.config.override('config', runner_conf_specific):
        runner = MPIRunner.create_from_conf_key('mpirunner_cfg')

        cfg_dict = runner_conf_specific['mpirunner_cfg']
        assert runner.cmd == cfg_dict['mpi_runner_cmd']
        assert runner.np_flags == cfg_dict['mpi_runner_np_flags']
        assert runner.pre_np_flags == cfg_dict['mpi_runner_pre_np_flags']
        assert runner.post_np_flags == cfg_dict['mpi_runner_post_np_flags']
        assert runner.full_cmd(2) == 'srun --pre --sflags 2 --post'
        assert runner.full_cmd(1) == 'srun --pre --sflags 1 --post'

        opts = runner.full_opts(2)
        assert len(opts) == 4
        assert opts[0] == runner.pre_np_flags
        assert opts[1] == runner.np_flags
        assert opts[2] == '2'
        assert opts[3] == runner.post_np_flags

    with spack.config.override('config', runner_conf_general):
        runner = MPIRunner.create_from_conf_key('nonexistent_conf')

        assert runner.cmd == runner_conf_general['mpi_runner_cmd']
        assert runner.np_flags == MPIRunner.default_np_flags
        assert runner.pre_np_flags == runner_conf_general['mpi_runner_pre_np_flags']
        assert runner.post_np_flags == ''

        opts = runner.full_opts()
        assert len(opts) == 3
        assert opts[0] == runner.pre_np_flags
        assert opts[1] == runner.np_flags
        assert opts[2] == '1'

        runner_2 = MPIRunner.create_from_conf(runner_conf_general)

        assert runner.cmd == runner_2.cmd
        assert runner.np_flags == runner_2.np_flags
        assert runner.pre_np_flags == runner_2.pre_np_flags
        assert runner.post_np_flags == runner_2.post_np_flags

    tmpdir_str = str(tmpdir)
    os.environ["PATH"] = tmpdir_str

    runner = MPIRunner.query_res_manager('srun', tmpdir_str)

    assert runner.cmd == fs.join_path(tmpdir_str, 'mpiexec')
    assert runner.np_flags == MPIRunner.default_np_flags
    assert runner.pre_np_flags == ''
    assert runner.post_np_flags == ''

    with tmpdir.as_cwd():
        fs.touch('srun')
        fs.set_executable('srun')
        runner = MPIRunner.query_res_manager('srun', tmpdir_str)
        assert runner.cmd.split('/')[-1] == 'srun'
        assert runner.np_flags == MPIRunner.default_np_flags
        assert runner.pre_np_flags == ''
        assert runner.post_np_flags == ''

        with spack.config.override('config', runner_conf_specific):
            runner = MPIRunner.create_def_runner(
                'test.mpirunner_cfg', tmpdir_str)

            cfg_dict = runner_conf_specific['mpirunner_cfg']
            assert runner.cmd == cfg_dict['mpi_runner_cmd']
            assert runner.np_flags == cfg_dict['mpi_runner_np_flags']
            assert runner.pre_np_flags == cfg_dict['mpi_runner_pre_np_flags']
            assert runner.post_np_flags == cfg_dict['mpi_runner_post_np_flags']
            assert runner.full_cmd(2) == 'srun --pre --sflags 2 --post'
            assert runner.full_cmd(1) == 'srun --pre --sflags 1 --post'

        runner = MPIRunner.create_def_runner('test.mpirunner_cfg', tmpdir_str)

        assert runner.cmd.split('/')[-1] == 'srun'
        assert runner.np_flags == MPIRunner.default_np_flags
        assert runner.pre_np_flags == ''
        assert runner.post_np_flags == ''
