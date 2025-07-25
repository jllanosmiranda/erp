function show_table_new_item(id){
    const table2 = document.getElementById(`${id}`)
    table2.style.display = "";

    const inputs = document.querySelectorAll(".supplier-contact-field");
    inputs.forEach(input => {
        input.readOnly = false;
        console.log("input to readonly")
    })

}

function edit_items(id){
    const row_view = document.getElementById(`${id}-view`);
    row_view.style.display = "none";

    const row_edit = document.getElementById(`${id}-edit`);
    row_edit.style.display = "";
    const inputs = row_edit.querySelectorAll(".supplier-contact-field");
    inputs.forEach(input => {
        input.readOnly = false;
        console.log("input to readonly")
    })

}

function add_new_product(){
    const table_supplier_product_list = document.getElementById('table-supplier-product-list')
    table_supplier_product_list.style.display = "none";

    const table_supplier_product_new = document.getElementById('table-supplier-product-new')
    table_supplier_product_new.style.display = "";
    const inputs = table_supplier_product_new.querySelectorAll(".new-product-field");
    inputs.forEach(input => {
        input.disabled = false;
    })
}


document.addEventListener('DOMContentLoaded', function() {
    const add_buttons = document.querySelectorAll('.add-item')
    add_buttons.forEach( button => {
        button.addEventListener('click', () => {
        show_table_new_item(button.getAttribute('data-table-body-id'))
        })
    })
    const edit_buttons = document.querySelectorAll('.edit-item-btn')
    edit_buttons.forEach(button => {
        button.addEventListener('click', () => {
            edit_items(button.getAttribute('data-form-id'))
        })
    })
    const add_new_product_button = document.querySelector('.create-new-item')
    add_new_product_button.addEventListener('click', () => {
        add_new_product()
    })
})
