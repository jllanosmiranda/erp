class Product {
    #price = 0
    #currency = ''
    #quantity = 0
    constructor(id, price, currency, quantity, subtotal_node){
        this.id = id
        this.subtotal_node = subtotal_node
        this.#price = price
        this.currency = currency
        this.#quantity = quantity
        this.subtotal_node.innerHTML = this.subtotal
    }

    set quantity(value){
        console.log("quantity changed")
        console.log(value)
        this.#quantity = value
        this.subtotal_node.innerHTML = this.subtotal
    }

    set price(value){
        this.#price = value
        this.subtotal_node.innerHTML = this.subtotal
    }

    get subtotal(){
        return this.#price * this.#quantity
    }
}

const products = []


function total(){
    let total =  0
    products.forEach(product => {
        total += product.subtotal
        console.log(product.subtotal)
        console.log(total)
    })
    const totalcell = document.getElementById("total-amount")
    totalcell.innerHTML = total
}


function add_up_amounts(){
    const prices_inputs = document.querySelectorAll('.price-field')
    prices_inputs.forEach((price_input, index) => {
        price_input.addEventListener('change', () => {
            console.log("price changed")
            products[index].price = price_input.value
            total()
        })
    })

    const quantity_inputs = document.querySelectorAll('.quantity-field')
    quantity_inputs.forEach((quantity_input, index) => {
        quantity_input.addEventListener('change', () => {
            console.log("quantity changed")
            products[index].quantity = quantity_input.value
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
                                        1,
                                        subtotals[index]
                                    )
                                    console.log("subtotal index")
                                    console.log(subtotals[index])
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
