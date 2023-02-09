# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    tick = fields.Boolean(string="Select Product")

    def btn_tick_untick(self):
        if self.tick == True:
            self.tick = False
        else:
            self.tick = True


class SaleOrder(models.Model):
    _inherit = "sale.order"

    extract_id = fields.Many2one(
        'sale.order', 'Extracted From', track_visibility="onchange", readonly=True, copy=False)
    split_id = fields.Many2one('sale.order', 'Splited From',
                               track_visibility="onchange", readonly=True, copy=False)
    extract_count = fields.Integer(
        'Extracted Quotes', compute='_compute_extract_count')
    split_count = fields.Integer(
        'Splited Quotes', compute='_compute_split_count')

    def _compute_extract_count(self):
        if self:
            for rec in self:
                rec.extract_count = 0
                extract_ids = self.env['sale.order'].sudo().search(
                    [('extract_id', '=', rec.id)])
                if extract_ids:
                    rec.extract_count = len(extract_ids.ids)

    def _compute_split_count(self):
        if self:
            for rec in self:
                rec.split_count = 0
                split_ids = self.env['sale.order'].sudo().search(
                    [('split_id', '=', rec.id)])
                if split_ids:
                    rec.split_count = len(split_ids.ids)

    def action_view_extract_quote(self):
        self.ensure_one()
        return{
            'name': 'Extracted Quotes',
            'res_model': 'sale.order',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'domain': [('extract_id', '=', self.id)],
            'target': 'current'
        }

    def action_view_split_quote(self):
        self.ensure_one()
        return{
            'name': 'Splited Quotes',
            'res_model': 'sale.order',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'domain': [('split_id', '=', self.id)],
            'target': 'current'
        }

    def action_split(self):
        return{
            'name': 'Split Quote',
            'res_model': 'sh.split.quote.wizard',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target': 'new'
        }

    def action_extract(self):

        do_unlink = False
        new_sale_order_id = False
        for rec in self:
            for line in rec.order_line:
                if line.tick:
                    do_unlink = True
            if do_unlink:
                new_sale_order = rec.copy()
                new_sale_order.extract_id = rec.id
                new_sale_order_id = new_sale_order
                for line in new_sale_order.order_line:
                    if not line.tick:
                        line.unlink()
                    else:
                        line.tick = False
            for line in rec.order_line:
                if line.tick:
                    line.tick = False
        if new_sale_order_id != False:
            return{
                'name': 'Quotation',
                'res_model': 'sale.order',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_id': new_sale_order_id.id,
                'domain': [('id', '=', new_sale_order_id.id)],
                'target': 'current',
            }

    def action_check(self):
        if self.order_line:
            for line in self.order_line:
                line.tick = True

    def action_uncheck(self):
        if self.order_line:
            for line in self.order_line:
                line.tick = False
