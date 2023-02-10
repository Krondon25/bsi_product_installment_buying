# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    check_cant = fields.Boolean('check real', default=False)

    @api.constrains('order_line')
    def _check_cant_purchase_order(self):
        if not self.check_cant :
            if self.po_extract_id:
                purchase_extract=self.env['purchase.order'].search([('id', '=',self.po_extract_id.id)])
                for products in purchase_extract.order_line:
                    if products.name == self.order_line.name :
                        products.product_qty = products.product_qty-self.order_line.product_qty
                        self.check_cant=True
                        purchase_extract.check_cant=True

