function show(queryExpresion){
    const view_cells = document.querySelectorAll(queryExpresion)
    view_cells.forEach(cell => {
        cell.classList.add("active")
    })

}

function hide(queryExpresion){
    const view_cells = document.querySelectorAll(queryExpresion)
    view_cells.forEach(cell => {
        cell.classList.remove("active")
    })
}


export function edit_product(){
    show(".basic-info .edit-input")
    hide(".basic-info .view-input")
    hide(`#edit-product`)
    show(`#save-product, #cancel-edit`)

}

export function view_product(){
    show(".basic-info .view-input")
    hide(".basic-info .edit-input")
    show(`#edit-product`)
    hide(`#save-product, #cancel-edit`)
}

function edit_supplier_product(supplier_product_id){
    show(`#supplier-product-edit-${supplier_product_id}`)
    hide(`#supplier-product-view-${supplier_product_id}`)
    hide(`#supplier-product-add`)

}

function cancel_edit_supplier_product(supplier_product_id){
    hide(`#supplier-product-edit-${supplier_product_id}`)
    show(`#supplier-product-view-${supplier_product_id}`)
    hide(`#supplier-product-add`)

}

document.addEventListener('DOMContentLoaded', function() {
    const edit_buttons = document.querySelectorAll('.edit-supplier-product-btn')
    edit_buttons.forEach(button => {
        button.addEventListener('click', () => {
            edit_supplier_product(button.getAttribute('data-supplier-product-id'))
        })
    })

    const cancel_edit_buttons = document.querySelectorAll('.cancel-edit-supplier-product-btn')
    cancel_edit_buttons.forEach(button => {
        button.addEventListener('click', () => {
            cancel_edit_supplier_product(button.getAttribute('data-supplier-product-id'))
        })
    })

    const add_button = document.getElementById('add-supplier-product')
    add_button.addEventListener('click', () => {
        const row = document.querySelectorAll('.supplier-product-new')
        row.style.display = "";
        const inputs = row.querySelectorAll(".supplier-product-field");
        inputs.forEach(input => {
            input.readOnly = false;
            console.log("input to readonly")
        })
    })
})



document.addEventListener('DOMContentLoaded', function() {
    const edit_button = document.getElementById('edit-product')
    edit_button.addEventListener('click', () => {
        edit_product()
    })

    const view_button = document.getElementById('cancel-edit')
    view_button.addEventListener('click', () => {
        view_product()
    })
})

