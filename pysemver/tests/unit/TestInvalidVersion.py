import nose.tools as nt

from pysemver import semantic

class TestInvalidVersin():
    def setup(self):
        pass

    def teardown(self):
        pass

    def test_InvalidVersion_is_Exception(self):
        '''
        Tests semantic.InvalidVersion is a base class for Exception
        '''
        nt.assert_is_instance(semantic.InvalidVersion(), Exception)

    def test_InvalidVersion_with_custom_exception_message(self):
        '''
        Tests when we raise InvalidVersion exception, that we get a custom
        error message.
        '''
        msg = semantic.InvalidVersion('my custom message')

        nt.eq_(msg.message, 'my custom message')
