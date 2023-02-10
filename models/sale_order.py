# -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"
    check_cant = fields.Boolean('check real', default=False)

    @api.constrains('order_line')
    def _check_cant_order(self):
        if not self.check_cant :
            if self.extract_id:
                sale_extract=self.env['sale.order'].search([('id', '=',self.extract_id.id)])
                for products in sale_extract.order_line:
                    if products.name == self.order_line.name :
                        products.product_uom_qty = products.product_uom_qty-self.order_line.product_uom_qty
                        self.check_cant=True
                        sale_extract.check_cant=True






