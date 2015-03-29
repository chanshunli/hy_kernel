'''
Test the hy kernel with JavaScript (well, CoffeeScript) tests
'''
import os
import sys
import signal
import time

from glob import glob

from hy_kernel import setup_assets

from IPython.testing import iptestcontroller


join = os.path.join

TEST_ROOT = os.path.dirname(__file__)

TESTS = glob(join(TEST_ROOT, 'test_*.coffee'))


class JSController(iptestcontroller.JSController):
    '''
    Maybe not the best way to run a specific set of tests...
    '''
    def __init__(self, *args, **kwargs):
        '''
        Create new test runner.
        '''
        super(JSController, self).__init__(*args, **kwargs)
        # get the test dir for utils
        ip_test_dir = iptestcontroller.get_js_test_dir()

        extras = [
            '--includes=%s' % join(ip_test_dir, 'util.js'),
            '--engine=%s' % self.engine
        ]

        self.cmd = ['casperjs', 'test'] + extras + TESTS

    def setup(self):
        '''
        let the super set up the temporary ipython dir, then install assets
        '''
        super(JSController, self).setup()
        # install the assets
        setup_assets(user=True, ipython_dir=self.ipydir.name)


def test_notebook():
    '''
    a nose-findable test
    '''
    controller = JSController('hy')
    exitcode = 1
    try:
        try:
            controller.setup()
            controller.launch(buffer_output=False)
        except Exception:
            import traceback
            traceback.print_exc()
            return controller, 1  # signal failure

        exitcode = controller.wait()
        return controller, exitcode
    except KeyboardInterrupt:
        return controller, -signal.SIGINT
    finally:
        controller.cleanup()
    assert exitcode == 0

if __name__ == '__main__':
    sys.exit(test_notebook())
