from .products import *
from .suppliers import *
from .supplier_product import *
from .purchase import *
from .good_receipt_notes import *

products = ['Product','']
suppliers = ['Supplier', 'SupplierContact', 'Bank', 'SupplierBankAccount']
supplier_product = ['SupplierProduct', 'SupplierProductPrice']
purchase = ['PurchaseRequirement', 'PurchaseRequirementItem','PurchaseOrder']
good_receipt_note = ['GoodReceiptNote', 'GoodReceiptNoteItem']
__all__ = products + suppliers + supplier_product