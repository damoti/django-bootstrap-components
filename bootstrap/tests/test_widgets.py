from datetime import date
from unittest import TestCase
from django import forms
from django.utils.translation import activate
from bootstrap import DateRangeField


class RangeForm(forms.Form):
    date_range = DateRangeField(localize=True, required=False, require_end=False)


class TestDateRangeField(TestCase):

    VALID_EN = '09/27/2017 ~ 10/14/2017'
    VALID_DE = '27.09.2017 ~ 14.10.2017'
    RANGE = (date(2017, 9, 27), date(2017, 10, 14))

    def test_initial_none(self):
        form = RangeForm()
        form.full_clean()
        self.assertEqual(form['date_range'].value(), '')

    def test_blank(self):
        form = RangeForm(data={'date_range': ''})
        form.full_clean()
        self.assertEqual(form['date_range'].value(), '')
        self.assertEqual(form.cleaned_data['date_range'], (None, None))

    def test_initial_range(self):
        activate('en')
        form = RangeForm(initial={'date_range': self.RANGE})
        form.full_clean()
        self.assertEqual(form['date_range'].value(), '2017-09-27 ~ 2017-10-14')

    def test_single_date_data(self):
        activate('en')
        single = self.VALID_EN.split('~')[0]
        form = RangeForm(data={'date_range': single})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form['date_range'].value(), single)
        self.assertEqual(form.cleaned_data['date_range'], (self.RANGE[0], None))

    def test_validation_cleaning_preparing_en(self):
        activate('en')
        form = RangeForm(data={'date_range': self.VALID_EN})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['date_range'], self.RANGE)
        self.assertEqual(form['date_range'].value(), self.VALID_EN)
        form = RangeForm(data={'date_range': self.VALID_DE})
        self.assertFalse(form.is_valid())

    def test_validation_cleaning_preparing_de(self):
        activate('de')
        form = RangeForm(data={'date_range': self.VALID_DE})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['date_range'], self.RANGE)
        self.assertEqual(form['date_range'].value(), self.VALID_DE)
        form = RangeForm(data={'date_range': self.VALID_EN})
        self.assertFalse(form.is_valid())
