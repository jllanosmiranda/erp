function add_contact(){
    const table2 = document.getElementById('contact-new-table')
    table2.style.display = "";

    const inputs = document.querySelectorAll(".supplier-contact-field");
    inputs.forEach(input => {
        input.readOnly = false;
        console.log("input to readonly")
    })

}

function edit_contact(id){
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


document.addEventListener('DOMContentLoaded', function() {
    const add_button = document.getElementById('add-contact-btn')
    add_button.addEventListener('click', () => {
        add_contact()

    })
    const edit_buttons = document.querySelectorAll('.edit-contact-btn')
    edit_buttons.forEach(button => {
        button.addEventListener('click', () => {
            edit_contact(button.getAttribute('data-contact-id'))
        })
    })
})
