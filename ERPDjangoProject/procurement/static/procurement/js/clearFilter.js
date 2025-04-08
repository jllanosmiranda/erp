
document.addEventListener("DOMContentLoaded", function() {
    var nav = document.getElementById("purchase");
    var subnav = nav.getElementsByClassName("sub-nav")[0];
    subnav.classList.replace("inactive","active");
})

function clearFilters() {
    document.getElementById('filter-form').reset();
    window.location.href = "/procurement/products/";
}