# Copyright (c) 2006-2008, 2010, 2013 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2014-2016 Claudiu Popa <pcmanticore@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import os
from os.path import exists


from pylint.checkers import initialize, imports
from pylint.lint import PyLinter

import pylint.testutils as testutils


class TestDependenciesGraph(object):
    """test the imports graph function"""

    dest = 'dependencies_graph.dot'

    def teardown_method(self):
        os.remove(self.dest)

    def test_dependencies_graph(self):
        imports._dependencies_graph(self.dest, {'labas': ['hoho', 'yep'],
                                                'hoho': ['yep']})
        with open(self.dest) as stream:
            assert stream.read().strip() == '''
digraph "dependencies_graph" {
rankdir=LR
charset="utf-8"
URL="." node[shape="box"]
"hoho" [];
"yep" [];
"labas" [];
"yep" -> "hoho" [];
"hoho" -> "labas" [];
"yep" -> "labas" [];
}
'''.strip()


class TestImportChecker(object):
    def setup_method(self):
        self.linter = l = PyLinter(reporter=testutils.TestReporter())
        initialize(l)

    def test_checker_dep_graphs(self):
        l = self.linter
        l.global_set_option('persistent', False)
        l.global_set_option('reports', True)
        l.global_set_option('enable', 'imports')
        l.global_set_option('import-graph', 'import.dot')
        l.global_set_option('ext-import-graph', 'ext_import.dot')
        l.global_set_option('int-import-graph', 'int_import.dot')
        l.global_set_option('int-import-graph', 'int_import.dot')
        # ignore this file causing spurious MemoryError w/ some python version (>=2.3?)
        l.global_set_option('ignore', ('func_unknown_encoding.py',))
        try:
            l.check('input')
            l.generate_reports()
            assert exists('import.dot')
            assert exists('ext_import.dot')
            assert exists('int_import.dot')
        finally:
            for fname in ('import.dot', 'ext_import.dot', 'int_import.dot'):
                try:
                    os.remove(fname)
                except:
                    pass

if __name__ == '__main__':
    import sys
    import pytest
    pytest.main(sys.argv)
