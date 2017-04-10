import sys
import io
import re
from test import context_test_case
from context.commands.contrib import bash

class TestBash(context_test_case.ContextTestCase):
    def test_is_contextualized(self):
        command = bash.Bash('ls', {}, [])
        args = self.get_args({
            'command': 'ls',
            'subcommand': []
        })

        original_output = sys.stdout
        sys.stdout = io.StringIO()
        command.run({'git': '~/git/example'}, args, [])
        output = sys.stdout.getvalue()
        sys.stdout = original_output

        scripts = output.split(';')
        self.assertTrue(re.match(r'^pushd .+\/git\/example.+', scripts[0]) is not None)
        self.assertEqual('ls', scripts[1].strip())
        self.assertEqual('popd > /dev/null', scripts[2].strip())


if __name__ == '__main__':
    unittest.main()
