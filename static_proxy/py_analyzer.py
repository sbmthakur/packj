#
# Based on MalOSS:  https://github.com/osssanitizer/maloss
#

import os
import ast
import logging
from os.path import basename

import asttokens

import proto.python.ast_pb2 as ast_pb2
from util.job_util import read_proto_from_file, write_proto_to_file, exec_command
from util.job_util import write_dict_to_file
from util.enum_util import LanguageEnum
from .static_base import StaticAnalyzer
from proto.python.ast_pb2 import PkgAstResults, AstLookupConfig

from static_proxy.astgen_py3 import py3_astgen
from static_proxy.astgen_py import py_astgen

class PyAnalyzer(StaticAnalyzer):
    def __init__(self):
        super(PyAnalyzer, self).__init__()
        self.language = LanguageEnum.python

    def exec_py2_astgen(analyze_path, outfile, configpath, root=None, pkg_name=None, pkg_version=None):
        try:
            astgen_py2_cmd = ['python', 'astgen_py.py', analyze_path, outfile, '-c', configpath]
            if root is not None:
                astgen_py2_cmd.extend(['-b', root])
            if pkg_name is not None:
                astgen_py2_cmd.extend(['-n', pkg_name])
            if pkg_version is not None:
                astgen_py2_cmd.extend(['-v', pkg_version])
            stdout, stderr, error = exec_command("python2 astgen", astgen_py2_cmd, cwd="static_proxy", redirect_mask=3)
            assert not error, "could not generate AST"
        except Exception as e:
            logging.debug("Failed to analyze for APIs using Python2: %s" % (str(e)))

    def astgen(self, inpath, outfile, root=None, configpath=None, pkg_name=None, pkg_version=None, evaluate_smt=False):
        analyze_path, is_decompress_path, outfile, root, configpath = self._sanitize_astgen_args(
            inpath=inpath, outfile=outfile, root=root, configpath=configpath, language=self.language)

        # default: python3
        try:
            # load the config proto
            configpb = AstLookupConfig()
            read_proto_from_file(configpb, configpath, binary=False)

            logging.debug("loaded lookup config from %s:\n%s", configpath, configpb)

            # invoke the language specific ast generators to call functions
            py3_astgen(inpath=analyze_path, outfile=outfile, configpb=configpb, root=root, pkg_name=pkg_name, pkg_version=pkg_version)

        # try python2
        except SyntaxError as se:
            logging.debug("Syntax error %s, now trying to parse %s again in python2!", se, analyze_path)
            self.exec_py2_astgen(analyze_path, outfile, configpath, root=root, pkg_name=pkg_name, pkg_version=pkg_version)
        except Exception as e:
            logging.debug("Fatal error %s running astgen for %s!" % (str(e), analyze_path))

        # clean up residue files
        self._cleanup_astgen(analyze_path=analyze_path, is_decompress_path=is_decompress_path)
