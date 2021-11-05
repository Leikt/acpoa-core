import os.path
import shutil
import unittest

from src.core.configuration import Configuration


class TestConfiguration(unittest.TestCase):
    PATH_TO_TEST = os.path.join('cfg', 'test_config.cfg')

    def setUp(self) -> None:
        original_path = os.path.join('cfg', 'test_config.cfg.original')
        shutil.copy(original_path, self.PATH_TO_TEST)

    def tearDown(self) -> None:
        os.remove(self.PATH_TO_TEST)

    def test_access_default(self):
        c = Configuration.open(self.PATH_TO_TEST)
        assert c.has_section('section1')
        assert c.has_section('section2')
        assert c.get('section1', 'opt1') == 'value1'

    def test_subsections(self):
        c = Configuration.open(self.PATH_TO_TEST)
        assert c.getboolean(c.subsection('section2', 'subsection1'), 'opt22')
        assert len(c.subsections_of('section2')) == 3
        assert len(c.subsections_of('section1')) == 0
        assert len(c.subsections_of('section2', 'subsection2')) == 1

        sub3 = c.subsections_of('section2', 'subsection2')[0]
        sub3_name = c.subsection_name(sub3)
        assert sub3_name == 'sub3'
        assert c.get(sub3, 'opt31') == 'value12'

    def test_set_boolean(self):
        c = Configuration.open(self.PATH_TO_TEST)
        c.setboolean('section2', 'bool', True)
        assert c.getboolean('section2', 'bool')
        c.setboolean('section2', 'bool', False)
        assert not c.getboolean('section2', 'bool')
        self.assertRaises(TypeError, c.setboolean, 'section2', 'bool', 'not_a_bool')
