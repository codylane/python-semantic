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

            exp_msg = 'Invalid version {0} must be numeric'.format(
                invalid_version
            )

            nt.eq_(actual_msg, exp_msg)

            # we raise InvalidVersion so that we get this test to pass since
            # we expect this test to raise InvalidVersion
            raise

    def test_major_property_returns_int(self):
        inst = semantic.Version('2016.01.18')

        nt.eq_(inst.major, 2016)
        nt.assert_is_instance(inst.major, int)

    def test_minor_propery_returns_int(self):
        inst = semantic.Version('1.2.3')

        nt.eq_(inst.minor, 2)
        nt.assert_is_instance(inst.minor, int)

    def test_patch_property_returns_init(self):
        inst = semantic.Version('4.5.6')

        nt.eq_(inst.patch, 6)
        nt.assert_is_instance(inst.patch, int)

    @mock.patch('pysemver.semantic.re.compile',
                autospec=True
                )
    def test_to_maj_min_patch_invokes_re_module_methods(self, mocked_method):
        '''
        to_maj_min_patch uses re to return a (major, minor, patch) tuple.
        * We want to make sure that re.compile is called with arguments
        * We want to make sure that the the compiled regex method .search
          is called with a version string.
        * We want to make sure that matcher.groups() is called and returns
          a (int, int, int)
        '''
        # re.compile('(\d+)\.?(\d+)?\.?(\d+)?').search('1.2.3').groups()
        mocked_method.return_value.search.return_value.groups.return_value = (1, 2, 3)

        # the Version.__init__ method invokes to_maj_min_patch.
        inst = semantic.Version('1.2.3')

        # assertion for re.compile('(\d+)\.?(\d+)?\.?(\d+)?')
        mocked_method.assert_called_once_with('(\d+)\.?(\d+)?\.?(\d+)?')

        # assertion for mmp_find.search('1.2.3')
        mocked_method.return_value.search.assert_called_once_with('1.2.3')

        # assertion for matcher.groups()
        mocked_method.return_value.search.return_value.groups.assert_called_once_with()

        nt.eq_(inst.to_maj_min_patch('1.2.3'), (1, 2, 3))

    @parameterized.expand([
        '1',
        '1.0',
        '1.2.0',
    ])
    @nt.nottest
    def test_maj_min_patch_returns_tuple(self):
        assert False, 'To implement'

    @parameterized.expand([
        '',
        'a.b.c',
    ])
    @nt.raises(semantic.InvalidVersion)
    @nt.nottest
    def test_maj_min_patch_returns_raises_InvalidVersion(self, invalid_version):
        assert False, 'To implement'

    @nt.nottest
    def test_to_list_returns_list(self):
        assert False, 'To implement'

    @nt.nottest
    def test__gt__invokes_compare_helper(self, mocked_method):
        assert False, 'To implement'

    @nt.nottest
    def test__gt__returns_True(self):
        assert False, 'To implement'

    @nt.nottest
    def test__gt__returns_False(self):
        assert False, 'To implement'

    @nt.nottest
    def test__ge__invokes_compare_helper(self, mocked_method):
        assert False, 'To implement'

    @nt.nottest
    def test__ge__returns_True(self):
        assert False, 'To implement'

    @nt.nottest
    def test__ge__returns_False(self):
        assert False, 'To implement'

    @nt.nottest
    def test__lt__invokes_compare_helper(self, mocked_method):
        assert False, 'To implement'

    @nt.nottest
    def test__lt__returns_True(self):
        assert False, 'To implement'

    @nt.nottest
    def test__lt__returns_False(self):
        assert False, 'To implement'

    @nt.nottest
    def test__le__invokes_compare_helper(self, mocked_method):
        assert False, 'To implement'

    @nt.nottest
    def test__le__returns_True(self):
        assert False, 'To implement'

    @nt.nottest
    def test__le__returns_False(self):
        assert False, 'To implement'

    @nt.nottest
    def test__eq__invokes_compare_helper(self, mocked_method):
        assert False, 'To implement'

    @nt.nottest
    def test__eq__returns_True(self):
        assert False, 'To implement'

    @nt.nottest
    def test__eq__returns_False(self):
        assert False, 'To implement'

    @nt.nottest
    def test__ne__invokes_compare_helper(self, mocked_method):
        assert False, 'To implement'

    @nt.nottest
    def test__ne__returns_True(self):
        assert False, 'To implement'

    @nt.nottest
    def test__ne__returns_False(self):
        assert False, 'To implement'

    @nt.nottest
    def test_compare_helper_returns_True(self):
        assert False, 'To implement'

    @nt.nottest
    def test_compare_helper_returns_False(self):
        assert False, 'To implement'
