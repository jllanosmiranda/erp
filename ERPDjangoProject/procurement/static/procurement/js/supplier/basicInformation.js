
export function edit_supplier(){
    const view_cells = document.querySelectorAll("td.view")
    view_cells.forEach(cell => {
        cell.style.display = "none";
    })

    const edit_cells = document.querySelectorAll("td.edit")
    edit_cells.forEach(cell => {
        cell.style.display = "";
    })
    document.querySelectorAll(".supplier-field").forEach(
        input => {
            input.readOnly = false;
            console.log("input to readonly")
        }
    )
}

export function view_supplier() {
    document.querySelectorAll(".supplier-field").forEach(
        input => {
            input.readOnly = true;
            console.log("input to readonly")
        }
    )
}

document.addEventListener('DOMContentLoaded', function() {
    const edit_button = document.getElementById('edit-supplier-basic-information')
    edit_button.addEventListener('click', () => {
        edit_supplier()
    })

    const view_button = document.getElementById('view-supplier-basic-information')
    view_button.addEventListener('click', () => {
        view_supplier()
    })
})
