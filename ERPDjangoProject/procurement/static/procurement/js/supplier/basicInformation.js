export function edit_supplier(root){
    const scope = root || document
    const viewBlocks = scope.querySelectorAll('.view-input')
    viewBlocks.forEach(block => {
        block.classList.remove('active')
    })

    const editBlocks = scope.querySelectorAll('.edit-input')
    editBlocks.forEach(block => {
        block.classList.add('active')
    })
}

export function view_supplier(root) {
    const scope = root || document
    const viewBlocks = scope.querySelectorAll('.view-input')
    viewBlocks.forEach(block => {
        block.classList.add('active')
    })

    const editBlocks = scope.querySelectorAll('.edit-input')
    editBlocks.forEach(block => {
        block.classList.remove('active')
    })
}

function initBasicSupplierButtons(){
    const edit_button = document.getElementById('edit-supplier-basic-information')
    if (edit_button) {
        edit_button.addEventListener('click', (e) => {
            const card = e.currentTarget.closest('.card') || document
            edit_supplier(card)
        })
    }

    const view_button = document.getElementById('view-supplier-basic-information')
    if (view_button) {
        view_button.addEventListener('click', (e) => {
            const card = e.currentTarget.closest('.card') || document
            view_supplier(card)
        })
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initBasicSupplierButtons)
} else {
    initBasicSupplierButtons()
}
