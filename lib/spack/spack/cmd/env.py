##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import llnl.util.tty as tty
import spack
import llnl.util.filesystem as fs
import spack.modules
import spack.util.spack_json as sjson
import spack.util.spack_yaml as syaml
import spack.cmd.install
import spack.cmd.uninstall
import spack.cmd.module
import spack.cmd.common.arguments as arguments
from spack.config import ConfigScope
from spack.spec import Spec, CompilerSpec, FlagMap
from spack.repository import Repo
from spack.version import VersionList
from contextlib import contextmanager

import argparse
try:
    from itertools import izip_longest as zip_longest
except ImportError:
    from itertools import zip_longest
import os
import sys
import shutil

description = "group a subset of packages"
section = "environment"
level = "long"

_db_dirname = fs.join_path(spack.var_path, 'environments')


class Environment(object):
    def __init__(self, name):
        self.name = name
        self.user_specs = list()
        self.concretized_order = list()
        self.specs_by_hash = dict()
        # Libs in this set must always appear as the dependency traced from any
        # root of link deps
        self.common_libs = dict()  # name -> hash
        # Packages in this set must always appear as the dependency traced from
        # any root of run deps
        self.common_bins = dict()  # name -> hash

    def add(self, user_spec):
        query_spec = Spec(user_spec)
        existing = set(x for x in self.user_specs
                       if Spec(x).name == query_spec.name)
        if existing:
            tty.die("Package {0} was already added to {1}"
                    .format(query_spec.name, self.name))
        self.user_specs.append(user_spec)

    def remove(self, query_spec):
        query_spec = Spec(query_spec)
        match_index = -1
        for i, spec in enumerate(self.user_specs):
            if Spec(spec).name == query_spec.name:
                match_index = i
                break

        if match_index < 0:
            tty.die("Not found: {0}".format(query_spec))

        del self.user_specs[match_index]
        if match_index < len(self.concretized_order):
            spec_hash = self.concretized_order[match_index]
            del self.concretized_order[match_index]
            del self.specs_by_hash[spec_hash]

    def concretize(self, force=False):
        if force:
            self.specs_by_hash = dict()
            self.concretized_order = list()

        num_concretized = len(self.concretized_order)
        new_specs = list()
        for user_spec in self.user_specs[num_concretized:]:
            tty.msg('Concretizing %s' % user_spec)
            spec = Spec(user_spec)
            spec.concretize()
            new_specs.append(spec)
            dag_hash = spec.dag_hash()
            self.specs_by_hash[dag_hash] = spec
            self.concretized_order.append(spec.dag_hash())
            sys.stdout.write(spec.tree(
                recurse_dependencies=True, install_status=True,
                hashlen=7, hashes=True))

        return new_specs

    def install(self, args):
        for concretized_hash in self.concretized_order:
            spec = self.specs_by_hash[concretized_hash]

            # Parse cli arguments and construct a dictionary
            # that will be passed to Package.do_install API
            kwargs = dict()
            spack.cmd.install.update_kwargs_from_args(args, kwargs)
            with pushd(self, args.output):
                spec.package.do_install(**kwargs)

    def uninstall(self, args):
        environment = read(args.environment)

        specs = environment._get_environment_specs(
            recurse_dependencies=True)

        args.all = False
        spack.cmd.uninstall.uninstall_specs(args, specs)

    def list(self, stream, **kwargs):
        for user_spec, concretized_hash in zip_longest(
                self.user_specs, self.concretized_order):

            stream.write('========= {0}\n'.format(user_spec))

            if concretized_hash:
                concretized_spec = self.specs_by_hash[concretized_hash]
                stream.write(concretized_spec.tree(**kwargs))

    def upgrade_dependency(self, dep_name, dry_run=False):
        """
        Note: if you have

        w -> x -> y

        and

        v -> x -> y

        Then if you upgrade y, you will start by re-concretizing w (and x).
        This should make sure that v uses the same x as w if this environment
        is supposed to reuse dependencies where possible. The difference
        compared to 'normal' concretization is that you want to keep things as
        similar as possible. I think the approach would be to go through all
        the common_libs and common_bins, recognize the first time they get
        re-concretized, and then replace them manually where encountered later.
        """
        new_order = list()
        new_deps = list()
        for i, spec_hash in enumerate(self.concretized_order):
            spec = self.specs_by_hash[spec_hash]
            if dep_name in spec:
                if dry_run:
                    tty.msg("Would upgrade {0} for {1}"
                            .format(spec[dep_name].format(), spec.format()))
                else:
                    new_spec = upgrade_dependency_version(spec, dep_name)
                    new_order.append(new_spec.dag_hash())
                    self.specs_by_hash[new_spec.dag_hash()] = new_spec
                    new_deps.append(new_spec[dep_name])
            else:
                new_order.append(spec_hash)

        if not dry_run:
            self.concretized_order = new_order
            return new_deps[0] if new_deps else None

    def reset_os_and_compiler(self, compiler=None):
        new_order = list()
        new_specs_by_hash = {}
        for spec_hash in self.concretized_order:
            spec = self.specs_by_hash[spec_hash]
            new_spec = reset_os_and_compiler(spec, compiler)
            new_order.append(new_spec.dag_hash())
            new_specs_by_hash[new_spec.dag_hash()] = new_spec
        self.concretized_order = new_order
        self.specs_by_hash = new_specs_by_hash

    def _get_environment_specs(self, recurse_dependencies):
        """Returns the specs of all the packages in an environment.
        At most one instance of any package gets added to the environment"""
        package_to_spec = {}
        spec_list = list()

        for spec_hash in self.concretized_order:
            spec = self.specs_by_hash[spec_hash]

            specs = spec.traverse(deptype=('link', 'run')) \
                if recurse_dependencies else (spec,)
            for dep in specs:
                if dep.name in package_to_spec:
                    tty.warn("{0} takes priority over {1}"
                             .format(package_to_spec[dep.name].format(),
                                     dep.format()))
                else:
                    package_to_spec[dep.name] = dep
                    spec_list.append(dep)

        return spec_list

    def to_dict(self):
        concretized_order = list(self.concretized_order)
        concrete_specs = dict()
        for spec in self.specs_by_hash.values():
            for s in spec.traverse():
                if s.dag_hash() not in concrete_specs:
                    concrete_specs[s.dag_hash()] = (
                        s.to_node_dict(all_deps=True))
        format = {
            'user_specs': self.user_specs,
            'concretized_order': concretized_order,
            'concrete_specs': concrete_specs,
        }
        return format

    @staticmethod
    def from_dict(name, d):
        c = Environment(name)
        c.user_specs = list(d['user_specs'])
        c.concretized_order = list(d['concretized_order'])
        specs_dict = d['concrete_specs']
        c.specs_by_hash = reconstitute(specs_dict, set(c.concretized_order))
        return c

    def path(self):
        return fs.join_path(_db_dirname, self.name)

    def config_path(self):
        return fs.join_path(self.path(), 'config')

    def repo_path(self):
        return fs.join_path(self.path(), 'repo')


def reconstitute(hash_to_node_dict, root_hashes):
    specs_by_hash = {}
    for dag_hash, node_dict in hash_to_node_dict.items():
        specs_by_hash[dag_hash] = Spec.from_node_dict(node_dict)

    for dag_hash, node_dict in hash_to_node_dict.items():
        for dep_name, dep_hash, deptypes in (
                Spec.dependencies_from_node_dict(node_dict)):
            specs_by_hash[dag_hash]._add_dependency(
                specs_by_hash[dep_hash], deptypes)

    return dict((x, y) for x, y in specs_by_hash.items() if x in root_hashes)


def reset_os_and_compiler(spec, compiler=None):
    spec = spec.copy()
    for x in spec.traverse():
        x.compiler = None
        x.architecture = None
        x.compiler_flags = FlagMap(x)
        x._concrete = False
        x._hash = None
    if compiler:
        spec.compiler = CompilerSpec(compiler)
    spec.concretize()
    return spec


def upgrade_dependency_version(spec, dep_name):
    spec = spec.copy()
    for x in spec.traverse():
        x._concrete = False
        x._hash = None
    spec[dep_name].versions = VersionList(':')
    spec.concretize()
    return spec


def write(environment, new_repo=None, config_files=None):
    """
    config_files will overwrite any existing config files in the environment.
    """
    tmp_new, dest, tmp_old = write_paths(environment)

    if os.path.exists(tmp_new) or os.path.exists(tmp_old):
        tty.die("Partial write state, run 'spack env repair'")

    fs.mkdirp(tmp_new)
    # create one file for the environment object
    with open(fs.join_path(tmp_new, 'environment.json'), 'w') as F:
        sjson.dump(environment.to_dict(), stream=F)

    dest_repo_dir = fs.join_path(tmp_new, 'repo')
    if new_repo:
        shutil.copytree(new_repo.root, dest_repo_dir)
    elif os.path.exists(environment.repo_path()):
        shutil.copytree(environment.repo_path(), dest_repo_dir)

    new_config_dir = fs.join_path(tmp_new, 'config')
    if os.path.exists(environment.config_path()):
        shutil.copytree(environment.config_path(), new_config_dir)
    else:
        fs.mkdirp(new_config_dir)

    if config_files:
        for cfg_path in config_files:
            dst_fname = os.path.basename(cfg_path)
            dst = fs.join_path(new_config_dir, dst_fname)
            shutil.copyfile(cfg_path, dst)

    if os.path.exists(dest):
        shutil.move(dest, tmp_old)
    shutil.move(tmp_new, dest)
    if os.path.exists(tmp_old):
        shutil.rmtree(tmp_old)


def write_paths(environment):
    tmp_new = fs.join_path(_db_dirname, "_" + environment.name)
    dest = environment.path()
    tmp_old = fs.join_path(_db_dirname, "." + environment.name)
    return tmp_new, dest, tmp_old


def repair(environment_name):
    """
    Possibilities:
        tmp_new, dest
        tmp_new, tmp_old
        tmp_old, dest
    """
    environment = Environment(environment_name)
    tmp_new, dest, tmp_old = write_paths(environment)
    if os.path.exists(tmp_old):
        if not os.path.exists(dest):
            shutil.move(tmp_new, dest)
        else:
            shutil.rmtree(tmp_old)
        tty.info("Previous update completed")
    elif os.path.exists(tmp_new):
        tty.info("Previous update did not complete")
    else:
        tty.info("Previous update may have completed")

    if os.path.exists(tmp_new):
        shutil.rmtree(tmp_new)


def read(environment_name):
    tmp_new, environment_dir, tmp_old = write_paths(
        Environment(environment_name))

    if os.path.exists(tmp_new) or os.path.exists(tmp_old):
        tty.die("Partial write state, run 'spack env repair'")

    with open(fs.join_path(environment_dir, 'environment.json'), 'r') as F:
        environment_dict = sjson.load(F)
    environment = Environment.from_dict(environment_name, environment_dict)

    return environment


# =============== Modifies Environment

def environment_create(args):
    environment = Environment(args.environment)
    if os.path.exists(environment.path()):
        raise tty.die("Environment already exists: " + args.environment)

    init_config = None
    if args.init_file:
        with open(args.init_file) as F:
            init_config = syaml.load(F)

    _environment_create(args.environment, init_config)


def _environment_create(name, init_config=None):
    environment = Environment(name)

    config_paths = None
    if init_config:
        user_specs = list()
        config_sections = {}
        for key, val in init_config.items():
            if key == 'user_specs':
                user_specs.extend(val)
            else:
                config_sections[key] = val

        for user_spec in user_specs:
            environment.add(user_spec)
        if config_sections:
            import tempfile
            tmp_cfg_dir = tempfile.mkdtemp()
            config_paths = []
        for key, val in config_sections.items():
            yaml_section = syaml.dump({key: val}, default_flow_style=False)
            yaml_file = '{0}.yaml'.format(key)
            yaml_path = fs.join_path(tmp_cfg_dir, yaml_file)
            config_paths.append(yaml_path)
            with open(yaml_path, 'w') as F:
                F.write(yaml_section)

    write(environment, config_files=config_paths)
    if config_paths:
        shutil.rmtree(tmp_cfg_dir)


def environment_update_config(args):
    environment = Environment(args.environment)
    write(environment, config_files=args.config_files)


def environment_add(args):
    environment = read(args.environment)
    for spec in spack.cmd.parse_specs(args.package):
        environment.add(spec.format())
    write(environment)


def environment_remove(args):
    environment = read(args.environment)
    for spec in spack.cmd.parse_specs(args.package):
        environment.remove(spec.format())
    write(environment)


def environment_concretize(args):
    environment = read(args.environment)
    _environment_concretize(environment, force=args.force)


def _environment_concretize(environment, force=False):
    """Function body separated out to aid in testing."""
    repo = prepare_repository(environment)
    prepare_config_scope(environment)

    # new_specs =
    environment.concretize(force=force)
    # Temporarily disable.
    # See https://github.com/spack/spack/issues/7878
    # for spec in new_specs:
    #    for dep in spec.traverse():
    #        dump_to_environment_repo(dep, repo)
    write(environment, repo)

# =============== Does not Modify Environment

def environment_install(args):
    environment = read(args.environment)
    prepare_repository(environment)
    environment.install(args)


def environment_uninstall(args):
    environment = read(args.environment)
    prepare_repository(environment)
    environment.uninstall(args)

# =======================================

def dump_to_environment_repo(spec, repo):
    dest_pkg_dir = repo.dirname_for_package_name(spec.name)
    if not os.path.exists(dest_pkg_dir):
        spack.repo.dump_provenance(spec, dest_pkg_dir)


def prepare_repository(environment, remove=None):
    # Temporarily disable.
    # See https://github.com/spack/spack/issues/7878
    return
    import tempfile
    repo_stage = tempfile.mkdtemp()
    new_repo_dir = fs.join_path(repo_stage, 'repo')
    if os.path.exists(environment.repo_path()):
        shutil.copytree(environment.repo_path(), new_repo_dir)
    else:
        spack.repository.create_repo(new_repo_dir, environment.name)
    if remove:
        remove_dirs = []
        repo = Repo(new_repo_dir)
        for pkg_name in remove:
            remove_dirs.append(repo.dirname_for_package_name(pkg_name))
        for d in remove_dirs:
            shutil.rmtree(d)
    repo = Repo(new_repo_dir)
    spack.repo.put_first(repo)
    return repo


def prepare_config_scope(environment):
    tty.debug("Check for config scope at " + environment.config_path())
    if os.path.exists(environment.config_path()):
        tty.msg("Using config scope at " + environment.config_path())
        ConfigScope(environment.name, environment.config_path())


def environment_relocate(args):
    environment = read(args.environment)
    prepare_repository(environment)
    environment.reset_os_and_compiler(compiler=args.compiler)
    write(environment)


def environment_list(args):
    # TODO? option to list packages w/ multiple instances?
    environment = read(args.environment)
    import sys
    environment.list(
        sys.stdout, recurse_dependencies=args.recurse_dependencies,
        hashes=args.long or args.very_long,
        hashlen=None if args.very_long else 7,
        install_status=args.install_status)


def environment_stage(args):
    environment = read(args.environment)
    prepare_repository(environment)
    for spec in environment.specs_by_hash.values():
        for dep in spec.traverse():
            dep.package.do_stage()


def environment_location(args):
    environment = read(args.environment)
    print(environment.path())


@contextmanager
def redirect_stdout(environment, ofname, defname):
    """Redirects STDOUT to (by default) a file within the environment;
    or else a user-specified filename."""
    if ofname == '-':
        yield
    else:
        path = os.path.join(environment.path(), defname) \
            if ofname is None else ofname
        with open(path, 'w') as f:
            original = sys.stdout
            sys.stdout = f
            yield
            sys.stdout = original


@contextmanager
def pushd(environment, odname):
    original = os.getcwd()
    os.chdir(environment.path() if odname is None else odname)
    yield
    os.chdir(original)


def environment_loads(args):
    # Set the module types that have been selected
    module_types = args.module_type
    if module_types is None:
        # If no selection has been made select all of them
        module_types = ['tcl']

    module_types = list(set(module_types))

    environment = read(args.environment)
    recurse_dependencies = args.recurse_dependencies
    args.recurse_dependencies = False
    with redirect_stdout(environment, args.output, 'loads.sh'):
        specs = environment._get_environment_specs(
            recurse_dependencies=recurse_dependencies)
        spack.cmd.module.loads(module_types, specs, args)


def environment_upgrade_dependency(args):
    environment = read(args.environment)
    repo = prepare_repository(environment, [args.dep_name])
    new_dep = environment.upgrade_dependency(args.dep_name, args.dry_run)
    if not args.dry_run and new_dep:
        dump_to_environment_repo(new_dep, repo)
        write(environment, repo)


def setup_parser(subparser):
    subparser.add_argument(
        'environment',
        help="The environment you are working with"
    )

    sp = subparser.add_subparsers(
        metavar='SUBCOMMAND', dest='environment_command')

    create_parser = sp.add_parser('create', help='Make an environment')
    create_parser.add_argument(
        '--init-file', dest='init_file',
        help='File with user specs to add and configuration yaml to use'
    )

    add_parser = sp.add_parser('add', help='Add a spec to an environment')
    add_parser.add_argument(
        'package',
        nargs=argparse.REMAINDER,
        help="Spec of the package to add"
    )

    remove_parser = sp.add_parser(
        'remove', help='Remove a spec from this environment')
    remove_parser.add_argument(
        'package',
        nargs=argparse.REMAINDER,
        help="Spec of the package to remove"
    )

    concretize_parser = sp.add_parser(
        'concretize', help='Concretize user specs')
    concretize_parser.add_argument(
        '-f', '--force', action='store_true',
        help="Re-concretize even if already concretized.")

    relocate_parser = sp.add_parser(
        'relocate',
        help='Reconcretize environment with new OS and/or compiler')
    relocate_parser.add_argument(
        '--compiler',
        help="Compiler spec to use"
    )

    list_parser = sp.add_parser('list', help='List specs in an environment')
    arguments.add_common_arguments(
        list_parser,
        ['recurse_dependencies', 'long', 'very_long', 'install_status'])

    loads_parser = sp.add_parser(
        'loads',
        help='List modules for an installed environment '
        '(see spack module loads)')
    spack.cmd.module.add_loads_arguments(loads_parser)
    loads_parser.add_argument(
        '-o', '--output', dest='output', default=None,
        help="Output file (or - for stdout); "
        "otherwise places in <env-location>/loads.sh")

    loads_parser = sp.add_parser(
        'location',
        help='Print the root directory of the environment')

    upgrade_parser = sp.add_parser(
        'upgrade',
        help='''Upgrade a dependency package in an environment to the latest
version''')
    upgrade_parser.add_argument(
        'dep_name', help='Dependency package to upgrade')
    upgrade_parser.add_argument(
        '--dry-run', action='store_true', dest='dry_run',
        help="Just show the updates that would take place")

    # stage_parser =
    sp.add_parser(
        'stage',
        help='Download all source files for all packages in an environment')

    config_update_parser = sp.add_parser(
        'update-config',
        help='Add config yaml file to environment')
    config_update_parser.add_argument(
        'config_files',
        nargs=argparse.REMAINDER,
        help="Configuration files to add"
    )

    install_parser = sp.add_parser(
        'install',
        help='Install all concretized specs in an environment')
    spack.cmd.install.add_common_arguments(install_parser)
    install_parser.add_argument(
        '-o', '--output', dest='output', default=None,
        help="Write install logs and setup files here "
        "(defaults to environment path)")

    uninstall_parser = sp.add_parser(
        'uninstall',
        help='Uninstall all concretized specs in an environment')
    spack.cmd.uninstall.add_common_arguments(uninstall_parser)


def env(parser, args, **kwargs):
    action = {
        'create': environment_create,
        'add': environment_add,
        'concretize': environment_concretize,
        'list': environment_list,
        'loads': environment_loads,
        'location': environment_location,
        'remove': environment_remove,
        'relocate': environment_relocate,
        'upgrade': environment_upgrade_dependency,
        'stage': environment_stage,
        'install': environment_install,
        'uninstall': environment_uninstall,
        'update-config': environment_update_config,
    }
    action[args.environment_command](args)
