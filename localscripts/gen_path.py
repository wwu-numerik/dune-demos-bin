#!/usr/bin/env python2.7

from __future__ import print_function, absolute_import, with_statement
from os.path import join

from localscripts import common


def gen_path():
    local_config = common.LocalConfig()
    with open(join(local_config.basedir, 'PATH.sh'), 'wb') as pathfile:
        # see common._prep_build_command on how to make this more elegant
        pathfile.write('export BASEDIR={}\n'.format(local_config.basedir))
        pathfile.write('export INSTALL_PREFIX={}\n'.format(local_config.install_prefix))
        pathfile.write('export PATH=${INSTALL_PREFIX}/bin:$PATH\n')
        pathfile.write('export LD_LIBRARY_PATH=${INSTALL_PREFIX}/lib64:${INSTALL_PREFIX}/lib:$LD_LIBRARY_PATH\n')
        pathfile.write(
            'export PKG_CONFIG_PATH=${INSTALL_PREFIX}/lib64/pkgconfig:${INSTALL_PREFIX}/lib/pkgconfig:${INSTALL_PREFIX}/share/pkgconfig:$PKG_CONFIG_PATH\n')
        pathfile.write('export CC={CC}\n'.format(CC=local_config.cc))
        pathfile.write('export CXX={CXX}\n'.format(CXX=local_config.cxx))
        pathfile.write('export F77={F77}\n'.format(F77=local_config.f77))
        pathfile.write('export PYTHON_VERSION=2.7\n')
        pathfile.write('[ -e ${INSTALL_PREFIX}/local/bin/activate ] && . ${INSTALL_PREFIX}/local/bin/activate\n')
        pathfile.write('export OMP_NUM_THREADS=1\n')
        pathfile.write('export SIMDB_PATH=${INSTALL_PREFIX}/DATA\n')
        pathfile.write('export QUEUE_DIRECTORY=${INSTALL_PREFIX}/QUEUE\n')


if __name__ == '__main__':
    gen_path()