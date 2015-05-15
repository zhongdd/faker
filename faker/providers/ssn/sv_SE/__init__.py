# coding=utf-8

from __future__ import unicode_literals
from .. import Provider as SsnProvider
import datetime
import random


class Provider(SsnProvider):

    @classmethod
    def ssn(cls):
        """
        Returns a 10 digit Swedish SSN, "Personnummer".
        Age of person is between 18 and 90
        years, based on local computer date. This function assigns random
        sex to person.

        It consists of 10 digits of the form YYMMDD-SSGQ, where
        YYMMDD is the date of birth, SS the state, G the gender
        number and Q the control character (Luhn checksum).

        http://en.wikipedia.org/wiki/Personal_identity_number_(Sweden)
        """
        def _luhn_checksum(number):
            def digits_of(n):
                return [int(d) for d in str(n)]
            digits = digits_of(number)
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = 0
            checksum += sum(odd_digits)
            for d in even_digits:
                checksum += sum(digits_of(d*2))
            return checksum % 10

        def _calculate_luhn(partial_number):
            check_digit = _luhn_checksum(int(partial_number) * 10)
            return check_digit if check_digit == 0 else 10 - check_digit

        min_age = 18 * 365
        max_age = 90 * 365
        age = datetime.timedelta(days=random.randrange(min_age, max_age))
        birthday = datetime.datetime.now() - age
        pnr_date = birthday.strftime('%y%m%d')
        suffix = str(random.randrange(0, 999)).zfill(3)
        checksum = str(_calculate_luhn(pnr_date + suffix))
        pnr = '{0}-{1}{2}'.format(pnr_date, suffix, checksum)

        return pnr
