from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from ..models import PurchaseRequirement, PurchaseRequirementItems, Supplier, SupplierProduct
from ..forms import PurchaseRequirementForm, purchase_requirement_items_formset
import logging
log = logging.getLogger(__name__)


@permission_required('procurement.view_purchaserequirement')
@login_required
def purchase_requirement_list(request):
    """
    View to display a list of purchase requirements with filtering options
    """
    # Get filter parameters from request
    supplier_id = request.GET.get('supplier')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status = request.GET.get('status')
    
    # Start with all purchase requirements
    purchase_requirements = PurchaseRequirement.objects.all().order_by('-created_at')
    
    # Apply filters if provided
    if supplier_id:
        # Get all purchase requirement items for this supplier
        items = PurchaseRequirementItems.objects.filter(
            supplier_product__supplier_id=supplier_id
        ).values_list('purchase_requirement_id', flat=True)
        purchase_requirements = purchase_requirements.filter(id__in=items)
    
    if start_date:
        purchase_requirements = purchase_requirements.filter(date__gte=start_date)
    
    if end_date:
        purchase_requirements = purchase_requirements.filter(date__lte=end_date)
    
    if status:
        purchase_requirements = purchase_requirements.filter(status=status)
    
    # Paginate results
    paginator = Paginator(purchase_requirements, 10)  # Show 10 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all suppliers for the filter dropdown
    suppliers = Supplier.objects.all()

    context = {
        'page_obj': page_obj,
        'suppliers': suppliers,
        'filter_supplier': supplier_id,
        'filter_start_date': start_date,
        'filter_end_date': end_date,
        'filter_status': status,
        'status_choices': PurchaseRequirement.status_choices,
    }
    
    return render(request, 'procurement/purchase_requirements/list.html', context)


@login_required
def purchase_requirement_create(request):
    """
    View to create a new purchase requirement
    """
    log.info("inside create")
    if request.method == 'POST':
        log.info("inside post")
        # Get the supplier ID from the form
        supplier_id = request.POST.get('supplier')
        supplier = None
        
        if supplier_id:
            supplier = get_object_or_404(Supplier, id=supplier_id)
        
        # Create the main form
        form = PurchaseRequirementForm(request.POST)
        
        # Create the formset with the supplier context
        formset = purchase_requirement_items_formset()(
            request.POST, 
            supplier=supplier
        )
        
        if form.is_valid() and formset.is_valid():
            log.info("valid formset")
            # Save the main form
            purchase_requirement = form.save(commit=False)
            purchase_requirement._changed_by = request.user
            purchase_requirement.save()
            
            # Save the formset
            formset.instance = purchase_requirement
            formset.save()
            
            messages.success(request, 'Requerimiento de compra creado exitosamente.')
            return redirect('purchase_requirement_list')
        else:
            log.info("invalid formset")
            log.info(form.errors)
            log.info(formset.errors)
    else:
        # Initial form and empty formset
        form = PurchaseRequirementForm(initial={'date': timezone.now().date(), 'status': 0})
        formset = purchase_requirement_items_formset()(supplier=None)

    # Get all suppliers for the dropdown
    suppliers = Supplier.objects.all()
    
    context = {
        'form': form,
        'formset': formset,
        'suppliers': suppliers,
    }
    
    return render(request, 'procurement/purchase_requirements/create.html', context)


@login_required
def purchase_requirement_detail(request, pk):
    """
    View to display details of a specific purchase requirement
    """
    purchase_requirement = get_object_or_404(PurchaseRequirement, pk=pk)
    items = PurchaseRequirementItems.objects.filter(purchase_requirement=purchase_requirement)
    
    # Calculate total
    total = sum(item.price * item.quantity for item in items)
    
    context = {
        'purchase_requirement': purchase_requirement,
        'items': items,
        'total': total,
    }
    
    return render(request, 'procurement/purchase_requirements/detail.html', context)


@login_required
def get_supplier_products(request, supplier_id):
    """
    AJAX view to get products for a specific supplier
    """
    supplier = get_object_or_404(Supplier, id=supplier_id)
    formset = purchase_requirement_items_formset()(supplier=supplier)
    context = {
        'formset': formset,
    }

    return render(request, 'procurement/purchase_requirements/product_options.html', context=context)


