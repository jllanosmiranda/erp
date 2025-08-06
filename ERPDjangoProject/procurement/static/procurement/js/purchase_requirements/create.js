document.addEventListener('DOMContentLoaded', function () {
    const mySelect = document.getElementById('supplier');

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
                    selectors.forEach(selector => {
                        selector.addEventListener('change', () => {
                            console.log('Selected value:', selector.id);
                            const other_selectos = document.querySelectorAll('.supplier-product-selector')
                            other_selectos.forEach(other_selector => {
                                if (other_selector.id !== selector.id){
                                    other_selector.value = ''
                                    other_selector.options[selector.selectedIndex].remove()
                                }
                            })

                            fetch(`/procurement/supplier-product/${selector.value}/`)
                                .then(response => response.json())
                                .then(data => {
                                    const price_id = selector.id.replace(/supplier_product$/, 'price')
                                    const currency_id = selector.id.replace(/supplier_product$/, 'currency')
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
