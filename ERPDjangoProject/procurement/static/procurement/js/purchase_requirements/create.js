
function update_selector_values(selector, selectedValues) {
   selectedValues.add(selector.value);
}

function update(selectors, selectedValues){
    selectors.forEach(selector => {
        const currentValue = selector.value;
        Array.from(selector.options).forEach(option => {

        })

    })
}

document.addEventListener('DOMContentLoaded', function () {
    const mySelect = document.getElementById('supplier');

    const selectedValues = new Set()

    mySelect.addEventListener('change',  () => {
        if (mySelect.value === ''){
            document.getElementById('items-container').innerHTML = null
        }
        else{
            console.log('Selected value:', mySelect.value);
            fetch(`/procurement/purchase-requirements/supplier-products/${mySelect.value}/`)
                .then(response => response.text())
                .then(data => {
                    document.getElementById('items-container').innerHTML = data
                    const selectors = document.querySelectorAll('.supplier-product-selector');
                    selectors.forEach(selectorChanged => {
                        selectorChanged.addEventListener('change', () => {
                            selectedValues.add(selectorChanged.value)
                            console.log('Selected value:', selectorChanged.id);
                            console.log('Selected value:', selectedValues);

                            const other_selectors = document.querySelectorAll('.supplier-product-selector')
                            other_selectors.forEach(other_selector => {
                                if (other_selector.id !== selectorChanged.id){
                                    Array.from(other_selector.options).forEach(option => {
                                        console.log("values")
                                        console.log(option.value)
                                        console.log(selectedValues.has(option.value))
                                        console.log(selectorChanged.value !== option.value)
                                        option.disabled = selectedValues.has(option.value) && other_selector.value !== option.value;
                                    })
                                }
                            })

                            fetch(`/procurement/supplier-product/${selectorChanged.value}/`)
                                .then(response => response.json())
                                .then(data => {
                                    const price_id = selectorChanged.id.replace(/supplier_product$/, 'price')
                                    const currency_id = selectorChanged.id.replace(/supplier_product$/, 'currency')
                                    const price_input = document.getElementById(price_id)
                                    const currency_input = document.getElementById(currency_id)
                                    price_input.value = data.price
                                    currency_input.value = data.currency
                                })
                        })
                    })
                })

        }
    })

})
