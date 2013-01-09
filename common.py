#!/usr/bin/env python

from __future__ import print_function
import os
from os.path import (join, exists)
import shutil
import subprocess
import sys

# define directories
_BASEDIR = os.path.abspath(join(os.path.dirname(sys.argv[0]), '..', '..'))
_SRCDIR = join(_BASEDIR, 'local', 'src')
try:
    os.mkdir(_SRCDIR)
except OSError, os_error:
    if os_error.errno != 17:
        raise os_error

def BASEDIR():
    return _BASEDIR

def SRCDIR():
    return _SRCDIR

_CC=''
_CXX=''
_F77=''
_CXXFLAGS=''
_config_opts_parsed=False

def _parse_config_opts():
    # use global variables
    global _CC
    global _CXX
    global _F77
    global _CXXFLAGS
    global _config_opts_parsed

    # get CC from environment
    env_CC=''
    try:
        env_CC=os.environ['CC']
    except AttributeError:
        raise Exception('ERROR: missing environment variable \'CC\'!')
    except KeyError:
        raise Exception('ERROR: missing environment variable \'CC\'!')
    except:
        raise

    # read corresponding config.opts
    config_opts_filename='config.opts.' + env_CC
    filename=join(_BASEDIR, config_opts_filename)
    print('reading from \'{filename}\':'.format(filename=config_opts_filename))
    try:
        config_opts = open(filename).read()
    except:
        raise Exception('ERROR: could not read from \'{filename}\'!'.format(filename=filename))
    config_opts = config_opts.replace('CONFIGURE_FLAGS=', '').replace('"', '').replace('\\', '').replace('\n', ' ')

    # read and remove CXXFLAGS first
    _CXXFLAGS = config_opts.split('CXXFLAGS')[1]
    config_opts = config_opts.split('CXXFLAGS')[0]
    if _CXXFLAGS[0] != '=':
        raise Exception('ERROR: no suitable \'CXXFLAGS=\'some_flags\'\' found in \'{filename}\'!'.format(filename=filename))
    _CXXFLAGS = _CXXFLAGS[1:]
    if _CXXFLAGS[0] == '\'':
        _CXXFLAGS = _CXXFLAGS[1:]
        tmp = _CXXFLAGS
        _CXXFLAGS = _CXXFLAGS[:_CXXFLAGS.index('\'')]
        config_opts += ' ' + tmp[tmp.index('\'') + 1:]
    else:
        tmp = _CXXFLAGS
        _CXXFLAGS = _CXXFLAGS.split(' ')[0]
        config_opts += ' ' + tmp[tmp.index(_CXXFLAGS) + len(_CXXFLAGS):]
    
    # then read CC, CXX and F77
    def find_that_is_not_one_of(string, rest):
        try:
            exceptional_msg='ERROR: no suitable \'{string}=some_exe\' found in \'{filename}\'!'.format(string=string,
                filename=filename)
            #print('config_opts = \'{config_opts}\''.format(config_opts=config_opts))
            after=config_opts[config_opts.index(string) + len(string):]
            #print('after = \'{after}\''.format(after=after))
            if after[0] != '=' or after[1] == ' ':
                raise Exception(exceptional_msg)
            possible=after[1:].split('=')[0].split()[0]
            if possible in rest:
                raise Exception(exceptional_msg)
            else:
                return possible
        except:
            raise
    
    _CC=find_that_is_not_one_of('CC', ['CXX', 'F77', 'CXXFLAGS'])
    _CXX=find_that_is_not_one_of('CXX', ['CC', 'F77', 'CXXFLAGS'])
    _F77=find_that_is_not_one_of('F77', ['CC', 'CXX', 'CXXFLAGS'])
    
    # print summary
    print('  CC={CC}'.format(CC=_CC))
    print('  CXX={CXX}'.format(CXX=_CXX))
    print('  CXXFLAGS=\'{CXXFLAGS}\''.format(CXXFLAGS=_CXXFLAGS))
    print('  F77={F77}'.format(F77=_F77))
    
    # finished
    _config_opts_parsed=True


# extract function
def extract_in_srcdir(tarfile, untared_name, target_name):
    if not exists(join(_SRCDIR, target_name)):
        if not exists(join(_SRCDIR, untared_name)):
            if exists(join(_SRCDIR, tarfile)):
                subprocess.call(['tar', 'xzf', tarfile], cwd=_SRCDIR)
            else:
                raise Exception('Error: %s does not exist'
                                % join(_SRCDIR, tarfile))
            shutil.move(join(_SRCDIR, untared_name), join(_SRCDIR, target_name))

def CC():
    if not _config_opts_parsed:
        _parse_config_opts()
    return _CC

def CXX():
    if not _config_opts_parsed:
        _parse_config_opts()
    return _CXX

def F77():
    if not _config_opts_parsed:
        _parse_config_opts()
    return _F77

def CXXFLAGS():
    if not _config_opts_parsed:
        _parse_config_opts()
    return _CXXFLAGS