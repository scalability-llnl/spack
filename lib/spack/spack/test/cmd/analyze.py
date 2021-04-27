# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pytest

import spack.config
import spack.package
import spack.cmd.install

from spack.spec import Spec
import spack.util.spack_json as sjson
from spack.main import SpackCommand

install = SpackCommand('install')
analyze = SpackCommand('analyze')


def test_test_package_not_installed(mock_fetch, install_mockery_mutable_config):
    # We cannot run an analysis for a package not installed
    out = analyze('run', 'libdwarf', fail_on_error=False)
    assert "==> Error: Spec 'libdwarf' matches no installed packages.\n" in out


def test_analyzer_get_install_dir(mock_fetch, install_mockery_mutable_config):
    """
    Test that we cannot get an analyzer directory without a spec package.
    """
    spec = Spec('libdwarf').concretized()
    assert 'libdwarf' in spack.analyzers.analyzer_base.get_analyzer_dir(spec)

    # Case 1: spec is missing attribute for package
    with pytest.raises(SystemExit):
        spack.analyzers.analyzer_base.get_analyzer_dir(None)

    class Packageless(object):
        package = None

    # Case 2: spec has package attribute, but it's None
    with pytest.raises(SystemExit):
        spack.analyzers.analyzer_base.get_analyzer_dir(Packageless())


def test_malformed_analyzer(mock_fetch, install_mockery_mutable_config):
    """
    Test that an analyzer missing needed attributes is invalid.
    """
    from spack.analyzers.analyzer_base import AnalyzerBase

    # Missing attribute description
    class MyAnalyzer(AnalyzerBase):
        name = "my_analyzer"
        outfile = "my_analyzer_output.txt"

    spec = Spec('libdwarf').concretized()
    with pytest.raises(SystemExit):
        MyAnalyzer(spec)


def test_analyze_output(tmpdir, mock_fetch, install_mockery_mutable_config):
    """
    Test that an analyzer errors if requested name does not exist.
    """
    install('libdwarf')
    install('python@3.8')
    analyzer_dir = tmpdir.join('analyzers')

    # An analyzer that doesn't exist should not work
    out = analyze('run', '-a', 'pusheen', 'libdwarf', fail_on_error=False)
    assert '==> Error: Analyzer pusheen does not exist\n' in out

    # We will output to this analyzer directory
    analyzer_dir = tmpdir.join('analyzers')
    out = analyze('run', '-a', 'install_files', '-p', str(analyzer_dir), 'libdwarf')

    # Ensure that if we run again without over write, we don't run
    out = analyze('run', '-a', 'install_files', '-p', str(analyzer_dir), 'libdwarf')
    assert "skipping" in out

    # With overwrite it should run
    out = analyze('run', '-a', 'install_files', '-p', str(analyzer_dir),
                  '--overwrite', 'libdwarf')
    assert "==> Writing result to" in out


def _run_analyzer(name, package, tmpdir):
    """
    A shared function to test that an analyzer runs.

    We return the output file for further inspection.
    """
    analyzer = spack.analyzers.get_analyzer(name)
    analyzer_dir = tmpdir.join('analyzers')
    out = analyze('run', '-a', analyzer.name, '-p', str(analyzer_dir), package)

    assert "==> Writing result to" in out
    assert "/%s/%s\n" % (analyzer.name, analyzer.outfile) in out

    # The output file should exist
    output_file = out.strip('\n').split(' ')[-1].strip()
    assert os.path.exists(output_file)
    return output_file


def test_installfiles_analyzer(tmpdir, mock_fetch, install_mockery_mutable_config):
    """
    test the install files analyzer
    """
    install('libdwarf')
    output_file = _run_analyzer("install_files", "libdwarf", tmpdir)

    # Ensure it's the correct content
    with open(output_file, 'r') as fd:
        content = sjson.load(fd.read())

    basenames = set()
    for key, attrs in content.items():
        basenames.add(os.path.basename(key))

    # Check for a few expected files
    for key in ['.spack', 'libdwarf', 'packages', 'repo.yaml', 'repos']:
        assert key in basenames


def test_environment_analyzer(tmpdir, mock_fetch, install_mockery_mutable_config):
    """
    test the environment variables analyzer.
    """
    install('libdwarf')
    output_file = _run_analyzer("environment_variables", "libdwarf", tmpdir)
    with open(output_file, 'r') as fd:
        content = sjson.load(fd.read())

    # Check a few expected keys
    for key in ['SPACK_CC', 'SPACK_COMPILER_SPEC', 'SPACK_ENV_PATH']:
        assert key in content

    # The analyzer should return no result if the output file does not exist.
    spec = Spec('libdwarf').concretized()
    env_file = os.path.join(spec.package.prefix, '.spack', 'spack-build-env.txt')
    assert os.path.exists(env_file)
    os.remove(env_file)
    analyzer = spack.analyzers.get_analyzer("environment_variables")
    analyzer_dir = tmpdir.join('analyzers')
    result = analyzer(spec, analyzer_dir).run()
    assert "environment_variables" in result
    assert not result['environment_variables']


def test_list_analyzers():
    """
    test that listing analyzers shows all the possible analyzers.
    """
    from spack.analyzers import analyzer_types

    # all cannot be an analyzer
    assert "all" not in analyzer_types

    # All types should be present!
    out = analyze('list-analyzers')
    for analyzer_type in analyzer_types:
        assert analyzer_type in out


def test_configargs_analyzer(tmpdir, mock_fetch, install_mockery_mutable_config):
    """
    test the config args analyzer.

    Since we don't have any, this should return an empty result.
    """
    install('libdwarf')
    analyzer_dir = tmpdir.join('analyzers')
    out = analyze('run', '-a', 'config_args', '-p', str(analyzer_dir), 'libdwarf')
    assert out == ''
