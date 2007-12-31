from textwrap import dedent

from simplsale.saletemplate import SaleTemplate


class TestSaleTemplate(object):

    def setUp(self):
        self.minimal = SaleTemplate('minimal')

    def test_receipt_text_all(self):
        values = dict(
            billing_email = 'abc@example.com',
            transaction_number = '123',
            billing_amount = '45.00',
            billing_street = '123 Fake St.',
            billing_city = 'Springfield',
            billing_state = 'OR',
            billing_zip = '97477',
            billing_card_number = '************5100',
            )
        expected = dedent("""\
        From: SimplSale-test@3purple.com
        To: abc@example.com
        Subject: SimplSale minimal - sale # 123

        The SimplTest minimal sale completed.

        The transaction number is 123.

        Billing amount was 45.00.

        Details:

        Billing Street: 123 Fake St.
        Billing City: Springfield
        BIlling State: OR
        Billing ZIP: 97477
        Billing Card No.: ************5100
        """)
        assert expected == self.minimal.receipt_text(**values)
