function subtotal(price_input_id, quantity_id){
    const price_input = document.getElementById(price_input_id)
    const quantity = document.getElementById(quantity_id)

    return price_input.value * quantity.value
}

function total(){
    let total =  0
    const prices_inputs = document.querySelectorAll('.price-field')
    prices_inputs.forEach(price_input => {
        total += price_input.value
        const totalcell = document.getElementById("total-amount")
        totalcell.innerHTML = total
     })
}

function add_up_amounts(){
    const prices_inputs = document.querySelectorAll('.price-field')
    console.log(prices_inputs)
    prices_inputs.forEach(price_input => {
        price_input.addEventListener('change', () => {
            const quantity_id = price_input.id.replace(/price$/, 'quantity')
            console.log(quantity_id)
            const sub = subtotal(price_input.id, quantity_id)
            console.log(sub)
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
                    add_up_amounts()
                    const selectors = document.querySelectorAll('.supplier-product-selector');
                    selectors.forEach(selectorChanged => {
                        selectorChanged.addEventListener('change', () => {
                            selectedValues.add(selectorChanged.value)

                            const other_selectors = document.querySelectorAll('.supplier-product-selector')
                            other_selectors.forEach(other_selector => {
                                if (other_selector.id !== selectorChanged.id){
                                    Array.from(other_selector.options).forEach(option => {
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
                                    total()
                                })
                        })
                    })

                })

        }
    })

})
