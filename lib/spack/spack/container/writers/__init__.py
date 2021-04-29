# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Writers for different kind of recipes and related
convenience functions.
"""
import collections
import copy

import spack.environment
import spack.schema.env
import spack.tengine as tengine
import spack.util.spack_yaml as syaml

from spack.container.images import data, build_info, commands_for
from spack.container.images import os_package_manager_for
from spack.container.images import bootstrap_template_for, checkout_command

#: Caches all the writers that are currently supported
_writer_factory = {}


def writer(name):
    """Decorator to register a factory for a recipe writer.

    Each factory should take a configuration dictionary and return a
    properly configured writer that, when called, prints the
    corresponding recipe.
    """
    def _decorator(factory):
        _writer_factory[name] = factory
        return factory
    return _decorator


def create(configuration, last_phase=None):
    """Returns a writer that conforms to the configuration passed as input.

    Args:
        configuration (dict): how to generate the current recipe
        last_phase (str): last phase to be printed or None to print them all
    """
    name = spack.environment.config_dict(configuration)['container']['format']
    return _writer_factory[name](configuration, last_phase)


def recipe(configuration, last_phase=None):
    """Returns a recipe that conforms to the configuration passed as input.

    Args:
        configuration (dict): how to generate the current recipe
        last_phase (str): last phase to be printed or None to print them all
    """
    return create(configuration, last_phase)()


def _stage_base_images(images_config):
    """Return a tuple with the base images to be used at the various stages.

    Args:
        images_config (dict): configuration under container:images
    """
    # If we have custom base images, just return them verbatim.
    build_stage = images_config.get('build', None)
    if build_stage:
        final_stage = images_config['final']
        return None, build_stage, final_stage

    # Check the operating system: this will be the base of the bootstrap
    # stage, if there, and of the final stage.
    operating_system = images_config.get('os', None)

    # Check the OS is mentioned in the internal data stored in a JSON file
    images_json = data()['images']
    if not any(os_name == operating_system for os_name in images_json):
        msg = ('invalid operating system name "{0}". '
               '[Allowed values are {1}]')
        msg = msg.format(operating_system, ', '.join(data()['images']))
        raise ValueError(msg)

    # Retrieve the build stage
    spack_info = images_config['spack']
    if isinstance(spack_info, dict):
        build_stage = 'bootstrap'
    else:
        spack_version = images_config['spack']
        image_name, tag = build_info(operating_system, spack_version)
        build_stage = 'bootstrap'
        if image_name:
            build_stage = ':'.join([image_name, tag])

    # Retrieve the bootstrap stage
    bootstrap_stage = None
    if build_stage == 'bootstrap':
        bootstrap_stage = images_json[operating_system]['bootstrap'].get(
            'image', operating_system
        )

    # Retrieve the final stage
    final_stage = images_json[operating_system].get(
        'final', {'image': operating_system}
    )['image']

    return bootstrap_stage, build_stage, final_stage


def _spack_checkout_config(images_config):
    spack_info = images_config['spack']

    url = 'https://github.com/spack/spack.git'
    ref = 'develop'
    resolve_sha, verify = False, False

    # Config specific values may override defaults
    if isinstance(spack_info, dict):
        url = spack_info.get('url', url)
        ref = spack_info.get('ref', ref)
        resolve_sha = spack_info.get('resolve_sha', resolve_sha)
        verify = spack_info.get('verify', verify)
    else:
        ref = spack_info

    return url, ref, resolve_sha, verify


class PathContext(tengine.Context):
    """Generic context used to instantiate templates of recipes that
    install software in a common location and make it available
    directly via PATH.
    """
    def __init__(self, config, last_phase):
        self.config = spack.environment.config_dict(config)
        self.container_config = self.config['container']

        # Operating system tag as written in the configuration file
        self.operating_system_key = self.container_config['images'].get('os')
        # Get base images and verify the OS
        bootstrap, build, final = _stage_base_images(
            self.container_config['images']
        )
        self.bootstrap_image = bootstrap
        self.build_image = build
        self.final_image = final

        # Record the last phase
        self.last_phase = last_phase

    @tengine.context_property
    def run(self):
        """Information related to the run image."""
        Run = collections.namedtuple('Run', ['image'])
        return Run(image=self.final_image)

    @tengine.context_property
    def build(self):
        """Information related to the build image."""
        Build = collections.namedtuple('Build', ['image'])
        return Build(image=self.build_image)

    @tengine.context_property
    def strip(self):
        """Whether or not to strip binaries in the image"""
        return self.container_config.get('strip', True)

    @tengine.context_property
    def paths(self):
        """Important paths in the image"""
        Paths = collections.namedtuple('Paths', [
            'environment', 'store', 'view'
        ])
        return Paths(
            environment='/opt/spack-environment',
            store='/opt/software',
            view='/opt/view'
        )

    @tengine.context_property
    def manifest(self):
        """The spack.yaml file that should be used in the image"""
        import jsonschema
        # Copy in the part of spack.yaml prescribed in the configuration file
        manifest = copy.deepcopy(self.config)
        manifest.pop('container')

        # Ensure that a few paths are where they need to be
        manifest.setdefault('config', syaml.syaml_dict())
        manifest['config']['install_tree'] = self.paths.store
        manifest['view'] = self.paths.view
        manifest = {'spack': manifest}

        # Validate the manifest file
        jsonschema.validate(manifest, schema=spack.schema.env.schema)

        return syaml.dump(manifest, default_flow_style=False).strip()

    @tengine.context_property
    def os_packages_final(self):
        """Additional system packages that are needed at run-time."""
        return self._os_packages_for_stage('final')

    @tengine.context_property
    def os_packages_build(self):
        """Additional system packages that are needed at build-time."""
        return self._os_packages_for_stage('build')

    @tengine.context_property
    def os_package_update(self):
        """Whether or not to update the OS package manager cache."""
        os_packages = self.container_config.get('os_packages', {})
        return os_packages.get('update', True)

    def _os_packages_for_stage(self, stage):
        os_packages = self.container_config.get('os_packages', {})
        package_list = os_packages.get(stage, None)
        return self._package_info_from(package_list)

    def _package_info_from(self, package_list):
        """Helper method to pack a list of packages with the additional
        information required by the template.

        Args:
            package_list: list of packages

        Returns:
            Enough information to know how to update the cache, install
            a list opf packages, and clean in the end.
        """
        if not package_list:
            return package_list

        image_config = self.container_config['images']
        image = image_config.get('build', None)

        if image is None:
            os_pkg_manager = os_package_manager_for(image_config['os'])
        else:
            os_pkg_manager = self.container_config['os_packages']['command']

        update, install, clean = commands_for(os_pkg_manager)

        Packages = collections.namedtuple(
            'Packages', ['update', 'install', 'list', 'clean']
        )
        return Packages(update=update, install=install,
                        list=package_list, clean=clean)

    @tengine.context_property
    def extra_instructions(self):
        Extras = collections.namedtuple('Extra', ['build', 'final'])
        extras = self.container_config.get('extra_instructions', {})
        build, final = extras.get('build', None), extras.get('final', None)
        return Extras(build=build, final=final)

    @tengine.context_property
    def labels(self):
        return self.container_config.get('labels', {})

    @tengine.context_property
    def bootstrap(self):
        """Information related to the build image."""
        images_config = self.container_config['images']
        bootstrap_recipe = None
        if self.bootstrap_image:
            config_args = _spack_checkout_config(images_config)
            command = checkout_command(*config_args)
            template_path = bootstrap_template_for(self.operating_system_key)
            env = tengine.make_environment()
            context = {"bootstrap": {
                "image": self.bootstrap_image,
                "spack_checkout": command
            }}
            bootstrap_recipe = env.get_template(template_path).render(**context)

        Bootstrap = collections.namedtuple('Build', ['image', 'recipe'])
        return Bootstrap(image=self.bootstrap_image, recipe=bootstrap_recipe)

    @tengine.context_property
    def render_build_phase(self):
        return not self.last_phase == 'bootstrap'

    @tengine.context_property
    def render_final_phase(self):
        return self.last_phase in (None, 'final')

    def __call__(self):
        """Returns the recipe as a string"""
        env = tengine.make_environment()
        t = env.get_template(self.template_name)
        return t.render(**self.to_dict())


# Import after function definition all the modules in this package,
# so that registration of writers will happen automatically
import spack.container.writers.singularity  # noqa
import spack.container.writers.docker  # noqa
