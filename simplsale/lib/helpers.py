"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
import datetime

from lxml.cssselect import CSSSelector
from lxml.etree import Element

from webhelpers import *


def fill_in_expiration_months(select):
    """Fill in expiration date month values in the given `select` element."""
    # First remove any children since they are just there to
    # help preview templates.
    for child in select.getchildren():
        select.remove(child)
    # Create the empty value option, selected since the form
    # is empty.
    e = Element('option', value='', selected='selected')
    e.text = '(select)'
    select.append(e)
    # Create months.
    for index, month_name in enumerate([
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November',
        'December',
        ]):
        month_number = index + 1
        e = Element('option', value='%02i' % month_number)
        e.text = '%02i (%s)' % (month_number, month_name)
        select.append(e)


def fill_in_expiration_years(select):
    """Fill in expiration date year values in the given `select` element."""
    # Remove existing children as above.
    for child in select.getchildren():
        select.remove(child)
    # Create the empty value option, selected since the form
    # is empty.
    e = Element('option', value='', selected='selected')
    e.text = '(select)'
    select.append(e)
    # Create options for 10 years, starting from this year.
    this_year = datetime.date.today().year
    for year in range(this_year, this_year + 10):
        year_abbrev = str(year)[-2:]
        e = Element('option', value=year_abbrev)
        e.text = '%s (%s)' % (year_abbrev, year)
        select.append(e)


def set_form_errors(form, error_text):
    """Set the form-errors element's text in the form."""
    form_errors = CSSSelector('#form-errors')(form)
    if error_text is None:
        # Remove form-errors if there is no error to report.
        for e in form_errors:
            e.getparent().remove(e)
    else:
        # Fill in form-errors with the text to report.
        for e in form_errors:
            # First get rid of anything lurking in the template.
            for c in e.getchildren():
                e.remove(c)
            # Now set the text.
            e.text = error_text


def field_names(form, required=False):
    """Return the names of the fields in `form`.

    Returns all names if `required` is `False`, or only the names of
    required fields if `required` is `True`.

    Takes care to provide a `billing_expiration` name if both the
    month and year fields are present for that field.
    """
    elements = CSSSelector('input[type!="submit"], select')(form)
    names = []
    for e in elements:
        name = e.attrib.get('name', None)
        if name is not None:
            names.append(name)
    if ('billing_expiration_month' in names
        and 'billing_expiration_year' in names
        and not 'billing_expiration' in names
        ):
        names.append('billing_expiration')
    return names


def remove_field_errors(form, *names):
    """Remove field error elements for each named field in `form`."""
    for name in names:
        if name.startswith('billing_expiration'):
            error_name = 'billing_expiration-errors'
        else:
            error_name = name + '-errors'
        errors = CSSSelector('[id$="%s"]' % error_name)(form)
        for e in errors:
            e.getparent().remove(e)


def set_field_value(form, name, value):
    """Set the value of a form's field."""
    inputs = CSSSelector('input[name="%s"]' % name)(form)
    for e in inputs:
        e.attrib['value'] = value
    selects = CSSSelector('select[name="%s"]' % name)(form)
    for e in selects:
        options = CSSSelector('option')(e)
        # Unselect any already-selected options.
        for o in options:
            if 'selected' in o.attrib:
                del o.attrib['selected']
        # Select the options that have the value.
        for o in options:
            if o.attrib['value'] == value:
                o.attrib['selected'] = 'selected'
