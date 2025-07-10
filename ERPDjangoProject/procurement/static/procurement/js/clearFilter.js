function clearFilters() {
    document.getElementById('filter-form').reset();
    window.location.href = "/procurement/products/";
}

function toggleEdit() {
    const div_edit = document.getElementById('products-edit');
    div_edit.style.display = "block";

    const div_view = document.getElementById('products-view');
    div_view.style.display = "none";
}

function toggleView() {
    const div_view = document.getElementById('products-view');
    div_view.style.display = "block";

    const div_edit = document.getElementById('products-edit');
    div_edit.style.display = "none";
}


document.addEventListener('DOMContentLoaded', () => {

    const button = document.getElementById('button-edit');
    button.addEventListener('click', () => {
        toggleEdit();
    });

    const button_view = document.getElementById('button-view');
    button_view.addEventListener('click', () => {
        toggleView();
    });
});
