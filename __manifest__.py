# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Dividir pedidos de Venta en pedidos parciales",
    "author": "TiEG",
    "website": "http://www.ti-eg.com",
    "support": "hola@ctieg.com",
    "license": "OPL-1",
    "category": "Extra Tools",
    "summary": "Dividir pedidos de Venta en pedidos parciales",

    "description": """Dividir pedidos de Venta en pedidos parciales.""",
    "version": "15.0.1",
    "depends": [
        "purchase",
        "sale_management"
    ],
    "application": True,
    "data": [
        "security/split_quo_security.xml",
        "security/ir.model.access.csv",
        "views/split_view.xml",
        "wizard/split_quote_wizard.xml",
        "wizard/split_rfq_wizard.xml",
        "views/sale_order.xml",
        "views/purchase_order.xml",
    ],

    "auto_install": False,
    "installable": True,

}
