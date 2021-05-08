# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest

import spack.config
import spack.paths
import spack.spec
import spack.modules.common
import spack.util.path


@pytest.fixture()
def modulefile_content(request):
    """Returns a function that generates the content of a module file
    as a list of lines.
    """

    writer_cls = getattr(request.module, 'writer_cls')

    def _impl(spec_str, module_set_name='default'):
        # Write the module file
        spec = spack.spec.Spec(spec_str)
        spec.concretize()
        generator = writer_cls(spec, module_set_name)
        generator.write(overwrite=True)

        # Get its filename
        filename = generator.layout.filename

        # Retrieve the content
        with open(filename) as f:
            content = f.readlines()
            content = ''.join(content).split('\n')
        generator.remove()
        return content

    return _impl


@pytest.fixture()
def update_template_dirs(config, monkeypatch):
    """Mocks the template directories for tests"""
    dirs = spack.config.get_config('config')['template_dirs']
    dirs = [spack.util.path.canonicalize_path(x) for x in dirs]
    monkeypatch.setattr(spack, 'template_dirs', dirs)


@pytest.fixture()
def factory(request):
    """Function that, given a spec string, returns an instance of the writer
    and the corresponding spec.
    """

    # Class of the module file writer
    writer_cls = getattr(request.module, 'writer_cls')

    def _mock(spec_string, module_set_name='default'):
        spec = spack.spec.Spec(spec_string)
        spec.concretize()
        return writer_cls(spec, module_set_name), spec

    return _mock
