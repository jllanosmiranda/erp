class Product {
    #price = 0
    #currency = ''
    #quantity = 0
    constructor(id, price, currency, subtotal_node){
        this.id = id
        this.subtotal_node = subtotal_node
        this.#price = price
        this.#currency = currency
        this.#quantity = 1
        this.subtotal_node.innerHTML = this.subtotal
    }

    set quantity(value){
        this.#quantity = Number(value)
        this.subtotal_node.innerHTML = this.subtotal.toFixed(2)
    }

    set price(value){
        this.#price = Number(value)
        this.subtotal_node.innerHTML = this.subtotal.toFixed(2)
    }

    get subtotal(){
        return this.#price * this.#quantity
    }

    get currency(){
        return this.#currency
    }

    set currency(value){
        this.#currency = Number(value)
    }
}

const products = []


function total(){
    let total_soles =  0
    let total_usd = 0
    let total_eur = 0
    products.forEach(product => {
        console.log(`currency ${product.currency} ${product.subtotal} ${typeof product.currency}`)
        if (product.currency === 0){
            total_soles += product.subtotal
        }
        if (product.currency === 1){
            total_usd += product.subtotal
        }
        if (product.currency === 2){
            total_eur += product.subtotal
        }
    })

    console.log(total_soles)
    console.log(total_usd)
    console.log(total_eur)

    const total_soles_object = document.getElementById("total-amount-soles")
    const total_usd_object = document.getElementById("total-amount-usd")
    const total_euros_object = document.getElementById("total-amount-euros")
    total_soles_object.innerHTML = total_soles.toFixed(2)
    total_usd_object.innerHTML = total_usd.toFixed(2)
    total_euros_object.innerHTML = total_eur.toFixed(2)
}


function add_up_amounts(){
    const prices_inputs = document.querySelectorAll('.price-field')
    prices_inputs.forEach((price_input, index) => {
        price_input.addEventListener('change', () => {
            products[index].price = price_input.value
            total()
        })
    })

    const quantity_inputs = document.querySelectorAll('.quantity-field')
    quantity_inputs.forEach((quantity_input, index) => {
        quantity_input.addEventListener('change', () => {
            products[index].quantity = quantity_input.value
            total()
        })
    })

    const currency_inputs = document.querySelectorAll('.currency-field')
    currency_inputs.forEach((currency_input, index) => {
        currency_input.addEventListener('change', () => {
            products[index].currency = currency_input.value
            total()
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
                    selectors.forEach((selectorChanged, index) => {
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
                                    const quantity_id = selectorChanged.id.replace(/supplier_product$/, 'quantity')
                                    const price_input = document.getElementById(price_id)
                                    const currency_input = document.getElementById(currency_id)
                                    const quantity_input = document.getElementById(quantity_id)
                                    quantity_input.value = 1
                                    const subtotals = document.querySelectorAll('.subtotal')
                                    price_input.value = data.price
                                    currency_input.value = data.currency
                                    products[index] = new Product(selectorChanged.value,
                                        data.price,
                                        data.currency,
                                        subtotals[index]
                                    )
                                    console.log(products)
                                    console.log(`index: ${index}`)
                                    total()
                                })
                        })
                    })

                })

        }
    })

})
