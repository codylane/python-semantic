#!/usr/bin/env python

import re

class InvalidVersion(Exception):
    pass

class Version(object):

    def __init__(self, version_str):
        self._major, self._minor, self._patch = self.to_maj_min_patch(version_str)

    @property
    def major(self):
        '''
        Returns the major version as an integer
        '''
        return self._major

    @property
    def minor(self):
        '''
        Returns the minor version as an integer
        '''
        return self._minor

    @property
    def patch(self):
        '''
        Returns the patch version as an integer
        '''
        return self._patch

    def to_maj_min_patch(self, version):
        '''
        Takes a string like 4.2.3 and converts it to major.minor.version

        @returns (major, minor, version) integer tuple
        @raises InvalidVersion if the version string is not parsable
        '''
        mmp_finder = re.compile('(\d+)\.?(\d+)?\.?(\d+)?')
        matcher = mmp_finder.search(version)
        if matcher is None:
            raise InvalidVersion('Invalid version %s must be numeric' %(version))

        major, minor, patch = matcher.groups()
        if minor is None: minor = '0'
        if patch is None: patch = '0'

        return int(major), int(minor), int(patch)

    def to_list(self):
        '''
        Converts to [self.major, self.minor. self.patch]
        '''
        return [self.major, self.minor, self.patch]

    def __gt__(self, other):
        '''
        Tests the current verion against another to see if v1 > v2

        @returns True if v1 > v2 otherwise return False
        '''
        return self._compare_helper(
            self.to_list(),
            other.to_list(),
            lt_zero_return=False,
            gt_zero_return=True,
            eq_zero_return=False
        )

    def __ge__(self, other):
        '''
        Tests the current verion against another to see if v1 >= v2

        @returns True if v1 >= v2 otherwise returns False
        '''
        return self._compare_helper(
            self.to_list(),
            other.to_list(),
            lt_zero_return=False,
            gt_zero_return=True,
            eq_zero_return=True
        )

    def __lt__(self, other):
        '''
        Tests the current version against another to see if v1 < v2

        @returns True if v1 < v2 otherwise returns False
        '''
        return self._compare_helper(
            self.to_list(),
            other.to_list(),
            lt_zero_return=True,
            gt_zero_return=False,
            eq_zero_return=False
        )

    def __le__(self, other):
        '''
        Tests the current version against another to see if v1 <= v2

        @returns True if v1 <= v2 otherwise returns False
        '''
        return self._compare_helper(
            self.to_list(),
            other.to_list(),
            lt_zero_return=True,
            gt_zero_return=False,
            eq_zero_return=True
        )

    def __eq__(self, other):
        '''
        Tests the current version against another to see if v1 == v2

        @returns True if v1 == v2 otherwise return False
        '''
        maj_diff = self.major - other.major
        min_diff = self.minor - other.minor
        pat_diff = self.patch - other.patch

        if maj_diff == 0 and min_diff == 0 and pat_diff == 0: return True
        return False

    def __ne__(self, other):
        '''
        Tests the current version against another to see if v1 != v2

        @returns True if v1 != v2 otherwise returns False
        '''
        maj_diff = self.major - other.major
        min_diff = self.minor - other.minor
        pat_diff = self.patch - other.patch

        if maj_diff == 0 and min_diff ==0 and pat_diff == 0: return False
        return True

    def _compare_helper(self, l1, l2, lt_zero_return, gt_zero_return, eq_zero_return, index=0):
        '''
        A neat little recursive helper utility for compairing versions.

        WARNING: This is not meant to be called directly outside of this module but is used by 
        this module to test things like v1 < v2.

        @param l1: A list [major, minor, patch]
        @param l2: A list [major, minor, patch]
        @param lt_zero_return: A boolean True of False
        @param gt_zero_return: A boolean True or False
        @param eq_zero_return: A boolean True or False

        @returns a boolean of the 
        '''
        items = zip(l1, l2)

        if index == len(items): return eq_zero_return

        val1, val2 = items[index]

        if val1 < val2:
            return lt_zero_return
        if val1 > val2:
            return gt_zero_return
        if val1 == val2:
            return self._compare_helper(l1, l2, lt_zero_return, gt_zero_return, eq_zero_return, index+1)
