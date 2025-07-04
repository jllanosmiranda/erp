from django.shortcuts import render

from ..forms import GoodReceiptNoteForm, form_set


def good_receipt_order(request):
    form = GoodReceiptNoteForm()
    context = {'form': form}
    return render(request, 'procurement/good_receipt_notes/goodReceiptNoteNew.html', context=context)


def good_receipt_note_list(request):
    pass


def good_receipt_note_supplier_products(request, supplier_id, extra=1):
    GoodReceiptNoteItemSet = form_set(extra=extra)
    print("request")
    print(request)
    print(request.GET)
    if request.method == 'GET':
        formset = GoodReceiptNoteItemSet(supplier_id=supplier_id, prefix='leo')
        context = {'formset': formset}
        return render(request, 'procurement/good_receipt_notes/goodReceiptNoteItem.html', context=context)
