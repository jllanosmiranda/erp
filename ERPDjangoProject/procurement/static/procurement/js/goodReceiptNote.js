import {AddFormSet} from "./suppliers.js";

var extra = 1
document.addEventListener('DOMContentLoaded', function() {
    const mySelect = document.getElementById('id_supplier');
    const items_list = document.getElementById('items-list')

    mySelect.addEventListener('change', function() {
        // Your function to execute on change
        myFunction(mySelect.value);
    });

    function myFunction(selectedValue) {
        console.log('Selected value:', selectedValue);
        fetch(`goods-products/${selectedValue}/${extra}`)
            .then(response => response.text())
            .then(data => {
                items_list.innerHTML = data
            })
        // Add your custom logic here
    }

});


function remove_option(selects){
    var selected_options = [];

    selects.forEach(select => {
        selected_options.push(select.value)
    })

    selects.forEach(select => {
            select.querySelectorAll('option')
                .forEach(option => {
                    if (selected_options.includes(option.value)){
                        option.classList.add("hidden-option")
                    }
                    else{
                        option.classList.remove("hidden-option")
                    }
                })
    })
}


export function handle_click(event, list_id, prefix ){
    const Selects = document.querySelectorAll('.dynamic-form select');

    if (Selects.length > 0){
        var total_options = Selects[0].querySelectorAll('option').length;
        var total_selects = Selects.length;
        if (total_selects <= total_options) {
            AddFormSet(event, list_id, prefix);
        }

    }

    remove_option(Selects);

    Selects.forEach(select => {
        select.addEventListener('change', selected => {
            remove_option(Selects);
        })
    })
}

window.handle_click = handle_click;
