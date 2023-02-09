# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields


class SplitQuoteWizard(models.TransientModel):
    _name = 'sh.split.quote.wizard'
    _description = 'Split Quote Wizard'

    split_by = fields.Selection(
        [('new', 'New'), ('existing', 'Existing')], default='new', string="Split By", required=True)
    sale_order_id = fields.Many2one('sale.order', string='Existing Quote', domain=[
                                    ('state', 'in', ['draft', 'sent'])])

    def action_split(self):
        active_id = self.env.context.get('active_id')
        active_so = self.env['sale.order'].sudo().browse(active_id)
        if self.split_by == 'existing':
            do_unlink = False
            new_sale_order_id = False
            for line in self.sale_order_id.order_line:
                if line.tick:
                    do_unlink = True
            if do_unlink:
                new_sale_order = self.sale_order_id.copy()
                new_sale_order.split_id = self.sale_order_id.id
                new_sale_order_id = new_sale_order
                for line in new_sale_order.order_line:
                    if not line.tick:
                        line.unlink()
                    else:
                        line.tick = False
            for line in self.sale_order_id.order_line:
                if line.tick:
                    line.unlink()
            if new_sale_order_id:
                return{
                    'name': 'Quotation',
                    'res_model': 'sale.order',
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_id': new_sale_order_id.id,
                    'domain': [('id', '=', new_sale_order_id.id)],
                    'target': 'current',
                }
        elif self.split_by == 'new':
            do_unlink = False
            new_sale_order_id = False
            for line in active_so.order_line:
                if line.tick:
                    do_unlink = True
            if do_unlink:
                new_sale_order = active_so.copy()
                new_sale_order.split_id = active_so.id
                new_sale_order_id = new_sale_order
                for line in new_sale_order.order_line:
                    if not line.tick:
                        line.unlink()
                    else:
                        line.tick = False
            for line in active_so.order_line:
                if line.tick:
                    line.unlink()
            if new_sale_order_id:
                return{
                    'name': 'Quotation',
                    'res_model': 'sale.order',
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_id': new_sale_order_id.id,
                    'domain': [('id', '=', new_sale_order_id.id)],
                    'target': 'current',
                }
