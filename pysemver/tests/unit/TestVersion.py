import nose.tools as nt
from nose_parameterized import parameterized

from pysemver import semantic

import mock

class TestVersion():
    def setup(self):
        pass

    def teardown(self):
        pass

    @parameterized.expand([
        '1.2.3',
        '2016.01.03',
    ])
    def test__init__does_not_raise_InvalidVersion(self, version):
        '''
        Make a couple of assertions and to our Version() and make sure that
        no error is raised
        '''
        inst = semantic.Version(version)

        nt.assert_is_instance(inst, semantic.Version)

        # we parse the version into a list so we make asserstions on what
        # the results should be.
        version_list = version.split('.', 2)

        nt.assert_true(len(version_list) == 3)

        # here is where we define what our expected major, minor, patch
        # should be
        exp_maj, exp_minor, exp_patch = [int(ver) for ver in version_list]

        nt.eq_(inst.major, exp_maj)
        nt.eq_(inst.minor, exp_minor)
        nt.eq_(inst.patch, exp_patch)

    @mock.patch.object(semantic.Version, 'to_maj_min_patch', autospec=True)
    def test__init__invokes_to_maj_min_patch_method(self, mocked_method):
        '''
        Since Version() calls an internal method
        self.to_maj_min_patch(version_str), we will make sure that this
        function is called.
        '''

        # we have to set a return value that matches the original signature
        #  for the mocked method because we expect a list to be returned.
        # If you comment this out you will get this error:
        # 'ValueError: need more than 0 values to unpack' because you will be
        # returning a mock object.
        mocked_method.return_value = [2016, 1, 12]

        inst = semantic.Version('2016.01.12')

        mocked_method.assert_called_once_with(inst, '2016.01.12')


    @parameterized.expand([
        '',
        'a.b.c',
    ])
    @nt.raises(semantic.InvalidVersion)
    def test__init__raises_InvalidVersion(self, invalid_version):
        # This try catch is here only because we want to capture
        # the error the exception message.  We will later make
        # an assertion on the custom message when we raise InvalidVersion
        try:
            inst = semantic.Version(invalid_version)

            # if we get here, then nose will tell us that the exception
            # was not raised, and this test will fail.
        except semantic.InvalidVersion as e:
            actual_msg = str(e)

            nt.eq_(actual_msg, 'Invalid version {0} must be numeric'.format(invalid_version))

            raise

