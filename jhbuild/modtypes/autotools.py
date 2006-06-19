# jhbuild - a build script for GNOME 1.x and 2.x
# Copyright (C) 2001-2006  James Henstridge
#
#   autotools.py: autotools module type definitions.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

__metaclass__ = type

import os

from jhbuild.errors import FatalError, BuildStateError
from jhbuild.modtypes import \
     Package, get_dependencies, get_branch, register_module_type

__all__ = [ 'AutogenModule' ]

class AutogenModule(Package):
    '''Base type for modules that are distributed with a Gnome style
    "autogen.sh" script and the GNU build tools.  Subclasses are
    responsible for downloading/updating the working copy.'''
    type = 'autogen'

    STATE_CHECKOUT       = 'checkout'
    STATE_FORCE_CHECKOUT = 'force_checkout'
    STATE_CLEAN          = 'clean'
    STATE_CONFIGURE      = 'configure'
    STATE_BUILD          = 'build'
    STATE_CHECK          = 'check'
    STATE_INSTALL        = 'install'

    def __init__(self, name, branch, autogenargs='', makeargs='',
                 dependencies=[], after=[],
                 supports_non_srcdir_builds=True,
                 autogen_sh='autogen.sh'):
        Package.__init__(self, name, dependencies, after)
        self.branch = branch
        self.autogenargs = autogenargs
        self.makeargs    = makeargs
        self.supports_non_srcdir_builds = supports_non_srcdir_builds
        self.autogen_sh = autogen_sh

    def get_srcdir(self, buildscript):
        return self.branch.srcdir

    def get_builddir(self, buildscript):
        if buildscript.config.buildroot and self.supports_non_srcdir_builds:
            d = buildscript.config.builddir_pattern % (
                os.path.basename(self.get_srcdir(buildscript)))
            return os.path.join(buildscript.config.buildroot, d)
        else:
            return self.get_srcdir(buildscript)

    def get_revision(self):
        return self.branch.branchname

    def do_start(self, buildscript):
        pass
    do_start.next_state = STATE_CHECKOUT
    do_start.error_states = []

    def skip_checkout(self, buildscript, last_state):
        # skip the checkout stage if the nonetwork flag is set
        return buildscript.config.nonetwork

    def do_checkout(self, buildscript):
        srcdir = self.get_srcdir(buildscript)
        builddir = self.get_builddir(buildscript)
        buildscript.set_action('Checking out', self)
        self.branch.checkout(buildscript)
        # did the checkout succeed?
        if not os.path.exists(srcdir):
            raise BuildStateError('source directory %s was not created'
                                  % srcdir)
    do_checkout.next_state = STATE_CONFIGURE
    do_checkout.error_states = [STATE_FORCE_CHECKOUT]

    def skip_force_checkout(self, buildscript, last_state):
        return False

    def do_force_checkout(self, buildscript):
        buildscript.set_action('Checking out', self)
        self.branch.force_checkout(buildscript)
    do_force_checkout.next_state = STATE_CONFIGURE
    do_force_checkout.error_states = [STATE_FORCE_CHECKOUT]

    def skip_configure(self, buildscript, last_state):
        # skip if nobuild is set.
        if buildscript.config.nobuild:
            return True

        # don't skip this stage if we got here from one of the
        # following states:
        if last_state in [self.STATE_FORCE_CHECKOUT,
                          self.STATE_CLEAN,
                          self.STATE_BUILD,
                          self.STATE_INSTALL]:
            return False

        # skip if the makefile exists and we don't have the
        # alwaysautogen flag turned on:
        builddir = self.get_builddir(buildscript)
        return (os.path.exists(os.path.join(builddir, 'Makefile')) and
                not buildscript.config.alwaysautogen)

    def do_configure(self, buildscript):
        builddir = self.get_builddir(buildscript)
        if buildscript.config.buildroot and not os.path.exists(builddir):
            os.makedirs(builddir)
        buildscript.set_action('Configuring', self)

        if buildscript.config.buildroot and self.supports_non_srcdir_builds:
            cmd = self.get_srcdir(buildscript) + '/' + self.autogen_sh
        else:
            cmd = './' + self.autogen_sh
        cmd += ' --prefix %s' % buildscript.config.prefix
        if buildscript.config.use_lib64:
            cmd += " --libdir '${exec_prefix}/lib64'"
        cmd += ' %s' % self.autogenargs

        # if we are using configure as the autogen command, make sure
        # we don't pass --enable-maintainer-mode, since it breaks many
        # tarball builds.
        if self.autogen_sh == 'configure':
            cmd = cmd.replace('--enable-maintainer-mode', '')
            
        buildscript.execute(cmd, cwd=builddir)
    do_configure.next_state = STATE_CLEAN
    do_configure.error_states = [STATE_FORCE_CHECKOUT]

    def skip_clean(self, buildscript, last_state):
        return (not buildscript.config.makeclean or
                buildscript.config.nobuild)

    def do_clean(self, buildscript):
        buildscript.set_action('Cleaning', self)
        cmd = '%s %s clean' % (os.environ.get('MAKE', 'make'), self.makeargs)
        buildscript.execute(cmd, cwd=self.get_builddir(buildscript))
    do_clean.next_state = STATE_BUILD
    do_clean.error_states = [STATE_FORCE_CHECKOUT, STATE_CONFIGURE]

    def skip_build(self, buildscript, last_state):
        return buildscript.config.nobuild

    def do_build(self, buildscript):
        buildscript.set_action('Building', self)
        cmd = '%s %s' % (os.environ.get('MAKE', 'make'), self.makeargs)
        buildscript.execute(cmd, cwd=self.get_builddir(buildscript))
    do_build.next_state = STATE_CHECK
    do_build.error_states = [STATE_FORCE_CHECKOUT, STATE_CONFIGURE]

    def skip_check(self, buildscript, last_state):
        return (not buildscript.config.makecheck or
                buildscript.config.nobuild)

    def do_check(self, buildscript):
        buildscript.set_action('Checking', self)
        cmd = '%s %s check' % (os.environ.get('MAKE', 'make'), self.makeargs)
        buildscript.execute(cmd, cwd=self.get_builddir(buildscript))
    do_check.next_state = STATE_INSTALL
    do_check.error_states = [STATE_FORCE_CHECKOUT, STATE_CONFIGURE]

    def skip_install(self, buildscript, last_state):
        return buildscript.config.nobuild

    def do_install(self, buildscript):
        buildscript.set_action('Installing', self)
        cmd = '%s %s install' % (os.environ.get('MAKE', 'make'), self.makeargs)
        buildscript.execute(cmd, cwd=self.get_builddir(buildscript))
        buildscript.packagedb.add(self.name, self.get_revision() or '')
    do_install.next_state = Package.STATE_DONE
    do_install.error_states = []


def parse_autotools(node, config, repositories, default_repo):
    id = node.getAttribute('id')
    autogenargs = ''
    makeargs = ''
    supports_non_srcdir_builds = True
    autogen_sh = 'autogen.sh'
    if node.hasAttribute('autogenargs'):
        autogenargs = node.getAttribute('autogenargs')
    if node.hasAttribute('makeargs'):
        makeargs = node.getAttribute('makeargs')
    if node.hasAttribute('supports-non-srcdir-builds'):
        supports_non_srcdir_builds = \
            (node.getAttribute('supports-non-srcdir-builds') != 'no')
    if node.hasAttribute('autogen-sh'):
        autogen_sh = node.getAttribute('autogen-sh')

    # override revision tag if requested.
    autogenargs += ' ' + config.module_autogenargs.get(id, config.autogenargs)
    makeargs += ' ' + config.module_makeargs.get(id, config.makeargs)

    dependencies, after = get_dependencies(node)
    branch = get_branch(node, repositories, default_repo)

    return AutogenModule(id, branch, autogenargs, makeargs,
                         dependencies=dependencies,
                         after=after,
                         supports_non_srcdir_builds=supports_non_srcdir_builds,
                         autogen_sh=autogen_sh)
register_module_type('autotools', parse_autotools)


# deprecated module types below:
def parse_cvsmodule(node, config, repositories, default_repo):
    id = node.getAttribute('id')
    module = None
    revision = None
    checkoutdir = None
    autogenargs = ''
    makeargs = ''
    supports_non_srcdir_builds = True
    if node.hasAttribute('module'):
        module = node.getAttribute('module')
    if node.hasAttribute('revision'):
        revision = node.getAttribute('revision')
    if node.hasAttribute('checkoutdir'):
        checkoutdir = node.getAttribute('checkoutdir')
    if node.hasAttribute('autogenargs'):
        autogenargs = node.getAttribute('autogenargs')
    if node.hasAttribute('makeargs'):
        makeargs = node.getAttribute('makeargs')
    if node.hasAttribute('supports-non-srcdir-builds'):
        supports_non_srcdir_builds = \
            (node.getAttribute('supports-non-srcdir-builds') != 'no')

    # override revision tag if requested.
    autogenargs += ' ' + config.module_autogenargs.get(id, config.autogenargs)
    makeargs += ' ' + config.module_makeargs.get(id, config.makeargs)

    dependencies, after = get_dependencies(node)

    for attrname in ['cvsroot', 'root']:
        if node.hasAttribute(attrname):
            try:
                repo = repositories[node.getAttribute(attrname)]
                break
            except KeyError:
                raise FatalError('Repository=%s not found for module id=%s. Possible repositories are %s' % (node.getAttribute(attrname), node.getAttribute('id'), repositories))
    else:
        repo = repositories.get(default_repo, None)
    branch = repo.branch(id, module=module, checkoutdir=checkoutdir,
                         revision=revision)

    return AutogenModule(id, branch, autogenargs, makeargs,
                         dependencies=dependencies,
                         after=after,
                         supports_non_srcdir_builds=supports_non_srcdir_builds)
register_module_type('cvsmodule', parse_cvsmodule)

def parse_svnmodule(node, config, repositories, default_repo):
    id = node.getAttribute('id')
    module = None
    checkoutdir = None
    autogenargs = ''
    makeargs = ''
    supports_non_srcdir_builds = True
    if node.hasAttribute('module'):
        module = node.getAttribute('module')
    if node.hasAttribute('checkoutdir'):
        checkoutdir = node.getAttribute('checkoutdir')
    if node.hasAttribute('autogenargs'):
        autogenargs = node.getAttribute('autogenargs')
    if node.hasAttribute('makeargs'):
        makeargs = node.getAttribute('makeargs')
    if node.hasAttribute('supports-non-srcdir-builds'):
        supports_non_srcdir_builds = \
            (node.getAttribute('supports-non-srcdir-builds') != 'no')

    # override revision tag if requested.
    autogenargs += ' ' + config.module_autogenargs.get(id, config.autogenargs)
    makeargs += ' ' + config.module_makeargs.get(id, config.makeargs)

    dependencies, after = get_dependencies(node)

    if node.hasAttribute('root'):
        repo = repositories[node.getAttribute('root')]
    else:
        repo = repositories.get(default_repo, None)
    branch = repo.branch(id, module=module, checkoutdir=checkoutdir)

    return AutogenModule(id, branch, autogenargs, makeargs,
                         dependencies=dependencies,
                         after=after,
                         supports_non_srcdir_builds=supports_non_srcdir_builds)
register_module_type('svnmodule', parse_svnmodule)

def parse_archmodule(node, config, repositories, default_repo):
    id = node.getAttribute('id')
    version = None
    checkoutdir = None
    autogenargs = ''
    makeargs = ''
    supports_non_srcdir_builds = True
    if node.hasAttribute('version'):
        version = node.getAttribute('version')
    if node.hasAttribute('checkoutdir'):
        checkoutdir = node.getAttribute('checkoutdir')
    if node.hasAttribute('autogenargs'):
        autogenargs = node.getAttribute('autogenargs')
    if node.hasAttribute('makeargs'):
        makeargs = node.getAttribute('makeargs')
    if node.hasAttribute('supports-non-srcdir-builds'):
        supports_non_srcdir_builds = \
            (node.getAttribute('supports-non-srcdir-builds') != 'no')

    autogenargs += ' ' + config.module_autogenargs.get(id, config.autogenargs)
    makeargs += ' ' + config.module_makeargs.get(id, makeargs)

    dependencies, after = get_dependencies(node)

    if node.hasAttribute('root'):
        repo = repositories[node.getAttribute('root')]
    else:
        repo = repositories.get(default_repo, None)
    branch = repo.branch(id, module=version, checkoutdir=checkoutdir)

    return AutogenModule(branch, autogenargs, makeargs,
                         dependencies=dependencies,
                         after=after,
                         supports_non_srcdir_builds=supports_non_srcdir_builds)
register_module_type('archmodule', parse_archmodule)
