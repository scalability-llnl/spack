# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# Improvements that can be made:
# 1. Add alpine / busybox base option
# 2. Add option to add custom environment or labels
# 3. Possibly %files section?
# 4. Logical to customize entrypoint?
# 5. If we don't need to build, recipe can be printed to screen
# 6. If built, should we move to some (spack owned) location?
# 7. Check if Singularity not installed

import argparse
import os
import tempfile

import llnl.util.filesystem
import llnl.util.tty as tty
import spack.tengine
import spack.util.executable

description = "use singularity to build containers with spack packages"
section = "build"
level = "long"

#: Wrapper to the 'singularity' command
singularity_cmd = spack.util.executable.Executable('singularity')


def setup_parser(subparser):
    '''setup the parser, meaning creating all needed arguments / options'''

    actions = subparser.add_subparsers(metavar='build|recipe', dest='action')

    # subcommands are added as a courtesy so the user interaction reads as
    # a sentence, e.g., "spack singularity <build|recipe> --image ...
    recipe = actions.add_parser('recipe', help='generate a recipe')
    build = actions.add_parser('build', help='generate, build a recipe (sudo)')

    # Add equivalent options to all subparsers
    for action in [recipe, build]:

        action.add_argument(
            'specs', nargs=argparse.REMAINDER, help="specs of packages")

        action.add_argument(
            '--bootstrap', action='store', type=str, default='docker',
            help='Singularity bootstrap (default: docker)')

        action.add_argument(
            '--working_dir', action='store', type=str, default=None,
            help='temporary working directory for recipe|build.')

        action.add_argument(
            '--name', action='store', type=str, default='container.sif',
            help='container name (default container.sif)')

        action.add_argument(
            '--from', action='store', dest="image", type=str,
            default='ubuntu:18.04',
            help='image or from string (From:<image>) (default ubuntu:18.04)')

        action.add_argument(
            '--helpstr', action='store', type=str, default=None,
            help='custom help string to describe the container')

        action.add_argument(
            '--distro', action='store', type=str, default='',
            choices=['centos', 'archlinux', 'ubuntu', 'debian', 'alpine'],
            help='Linux distribution type of the base image'
            '(default: try to determine from the base image name)')

        action.add_argument(
            '--branch', action='store', type=str,
            default='develop',
            help='branch of Spack to deploy (default: develop)')

        action.add_argument(
            '--repo', action='store', type=str,
            default='spack',
            help='name of spack repository owner (default: spack)')


def singularity(parser, args):

    if not args.specs:
        tty.die("Please specify at least one spec (package) to install.")

    specs = ' '.join(args.specs)
    tty.msg("Installing packages %s" % specs)

    # Singularity %help section provides information about the container
    # via "singularity help <container>. If a help string isn't provided,
    # share the packages installed.
    help_str = args.helpstr
    if help_str is None:
        help_str = "This is a spack container with packages %s" % specs

    # Can we infer the distro from the base image?
    distro = get_distro(args.distro, args.image)

    # If we can't, the user needs to provide it.
    if distro == "":
        tty.die("Cannot infer distro, please set via --distro.")

    # Create the singularity recipe in a build directory
    build_dir = create_recipe(specs=specs,
                              image=args.image,
                              distro=distro,
                              bootstrap=args.bootstrap,
                              branch=args.branch,
                              repo=args.repo,
                              help=help_str,
                              build_dir=args.working_dir)

    # Build the container, or show how to do it?
    if args.action == "recipe":
        recipe_path = "%s/Singularity" % build_dir
        tty.msg("sudo singularity build container.sif %s" % recipe_path)

    else:

        # First ensure that Singularity is installed
        if not check_installed('singularity'):
            tty.die("singularity must be installed for build. Try recipe.")

        with llnl.util.filesystem.working_dir(build_dir):
            tty.msg('Building container for "%s"' % args.image)
            singularity_cmd('build', args.name, 'Singularity')

        # Check if the final container was built
        container = os.path.join(build_dir, args.name)
        if not os.path.exists(container):

            # Should we clean up?
            tty.die("Container build failed.")

        tty.msg("Container successfully built:", container)


def check_installed(name):
    '''check if Singularity is installed, required for build.
    '''
    singularity = spack.util.executable.which(name)
    if singularity is None:
        return False
    return True


def get_distro(distro, image):
    '''get distro will attempt to infer the distribution from the base image.

       Parameters
       ==========
       distro: a string to identify the distribution, one of centos, debian,
               or alpinelinux (should add alpine)
       image: the "From:" image
    '''
    if distro == '':
        tty.msg("Attempting to infer distro from base image...")
        for contender in ["archlinux", "debian", "centos", "ubuntu", "alpine"]:
            if contender in image:
                tty.msg("Found distro %s" % contender)
                distro = contender
                break

    # If the user provided ubuntu, it's debian
    if distro == 'ubuntu':
        distro = 'debian'

    return distro


def create_recipe(bootstrap,
                  image,
                  branch,
                  repo,
                  help,
                  specs,
                  distro,
                  build_dir):

    ''' create_recipe will start with the Singularity template, add
        dependencies, and return a populated recipe file.

        Parameters
        ==========
        bootstrap (str): the kind of bootstrap to do (default is docker)
        image (str): base image for the build (the From: block)
        branch (str): branch of the Spack repository to checkout (develop)
        repo (str): Spack repository to checkout (spack/spack)
        help (str): the help string to provide to the container
        specs (str): space separated list of packages (specs) to install
        distro (str) the OS distibution, if not obvious from name
        build_dir (str): the temporary directory to write / build in.
   '''

    # Dependencies based on base
    dependencies = {
        'centos': '''yum -y update && \\
    yum -y install git gcc gcc-c++ gcc-gfortran make bzip2 patch file
    ''',
        'debian': '''apt-get update && \\
    apt-get install -y git gcc g++ gfortran make bzip2 && \\
    apt-get install -y patch file curl python gnupg2 xz-utils && \\
    rm -rf /var/lib/apt/lists/*
    ''',
        'archlinux': '''pacman -Syu && \\
    pacman -Sy --noconfirm  \\
    base-devel ca-certificates curl \\
    gcc gcc-fortran git gnupg2 iproute2 \\
    make openssh python sudo tcl
    ''',
        'alpine': '''apk update && \\
    apk add --no-cache git gcc g++ gfortran make bzip2 && \\
    apk add --no-cache patch file curl python gnupg xz && \\
    apk add --no-cache curl bash openssh libtool linux-headers
    '''
    }

    # Double check we have a valid distro
    if distro not in dependencies:
        choices = "debian, centos, archlinux, alpine"
        tty.die("%s is not a valid choice, should be in %s" % choices)

    # Create a temporary build directory
    if build_dir is None:
        build_dir = tempfile.mkdtemp()

    if not os.path.exists(build_dir):
        tty.die("Working directory %s does not exist." % build_dir)

    recipe = os.path.join(build_dir, 'Singularity')

    # Singularity recipe template to build container
    template_recipe = os.path.join('containers', 'singularity', 'Singularity')
    template = spack.tengine.make_environment().get_template(template_recipe)

    # Tell the user what's going on!
    tty.msg("Working directory created in %s" % build_dir)
    tty.msg("Writing recipe to %s/Singularity" % build_dir)

    with open(recipe, 'w') as filey:
        filey.write(template.render({
            'bootstrap': bootstrap,
            'specs': specs,
            'help': help,
            'image': image,
            'dependencies': dependencies[distro],
            'branch': branch,
            'repo': repo
        }))

    return build_dir
