const USD = 0
const SOLES = 1
const EURO = 2



class ItemRow {
    #rowNode = null
    #subtotalNode = null
    #priceNode = null
    #currencyNode = null
    #quantityNode = null
    #supplierProductSelectorNode = null
    #itemChangedEvents = []
    #supplierProductSelectorChangedEvents = []

    constructor(rowNode){
        this.#rowNode = rowNode
        this.#subtotalNode = this.#rowNode.querySelector('.subtotal')
        this.#priceNode = this.#rowNode.querySelector('.price-field')
        this.#currencyNode = this.#rowNode.querySelector('.currency-field')
        this.#quantityNode = this.#rowNode.querySelector('.quantity-field')
        this.#supplierProductSelectorNode = this.#rowNode.querySelector('.supplier-product-selector')

        this.#priceNode.addEventListener('change', () => {
            this.updateSubTotal()
            this.#supplierProductSelectorChangedEvents.forEach(event => {
                event()
            })
        })

        this.#currencyNode.addEventListener('change', () => {
            this.updateSubTotal()
            this.#supplierProductSelectorChangedEvents.forEach(event => {
                event()
            })
        })

        this.#quantityNode.addEventListener('change', () => {
            this.updateSubTotal()
            this.#supplierProductSelectorChangedEvents.forEach(event => {
                event()
            })
        })

        this.#supplierProductSelectorNode.addEventListener('change', () => {
            fetch(`/procurement/supplier-product/${this.#supplierProductSelectorNode.value}/`)
                .then(response => response.json())
                .then(data => {
                    this.#priceNode.value = data.price
                    this.#currencyNode.value = data.currency
                    this.#quantityNode.value = 1
                    this.updateSubTotal()
                    console.log("event create a new item")
                    this.#supplierProductSelectorChangedEvents.forEach(event => {
                        event()
                    })
                })
        })
    }

    get supplierProductId(){
        return this.#supplierProductSelectorNode.value
    }

    get price(){
        return Number(this.#priceNode.value)
    }

    get currency(){
        return Number(this.#currencyNode.value)
    }

    get quantity(){
        return Number(this.#quantityNode.value)
    }

    get subtotal(){
        return this.price * this.quantity
    }


    get supplierProductSelectorNode(){
        return this.#supplierProductSelectorNode
    }

    addSupplierProductSelectorChangedEvent(event){
        this.#supplierProductSelectorChangedEvents.push(event)
    }


    updateSubTotal(){
        this.#subtotalNode.innerHTML = this.subtotal.toFixed(2)
    }

}

const products = []

class ItemListManager {
    #itemRows = []
    #total_soles = 0
    #total_usd = 0
    #total_eur = 0
    #selectedOptions = new Set()
    constructor(itemRowsNodes){
        const nodes_array = Array.from(itemRowsNodes)

        this.#itemRows = nodes_array.map(itemRowNode => new ItemRow(itemRowNode))
        this.#itemRows.forEach(itemRow => {
            itemRow.addSupplierProductSelectorChangedEvent(this.compute_totals.bind(this))
        })
        console.log(this.#itemRows)
    }

    optionsUsedUpdate(selectorChanged){
        console.log("options used update")
        const selectedValues = new Set()
        this.#itemRows.forEach(itemRow => {
            console.log("item row selected values")
            console.log(itemRow.item)
            if (itemRow.supplierProductSelectorNode.value !== null){
                const selector = itemRow.supplierProductSelectorNode
                selectedValues.add(selector.value)
                console.log(" item row selected values with items")
                console.log(itemRow)
            }

        })

        console.log("itemrows")
        console.log(this.#itemRows)
        console.log("selected values")
        console.log(this.#selectedOptions)

        this.#itemRows.forEach(itemRow => {
            const selector = itemRow.supplierProductSelectorNode
            if (selector.id !== selectorChanged.id){
                Array.from(selector.options).forEach(option => {
                    option.disabled = selectedValues.has(option.value) && selector.value !== option.value;
                })
            }
        })

    }

    get itemRows(){
        return this.#itemRows
    }

    compute_totals(){
        console.log("compute totals")
        this.#total_soles = 0
        this.#total_usd = 0
        this.#total_eur = 0
        this.#itemRows.forEach(itemRow => {
            console.log("item row supplierProduct")
            console.log(itemRow.supplierProductId)
            console.log(itemRow.subtotal)
            console.log(itemRow.currency)
            console.log(itemRow.supplierProductId === "")
            if (itemRow.supplierProductId === null){
                return
            }
            if (itemRow.currency === USD){
                this.#total_usd += itemRow.subtotal
            }
            if (itemRow.currency === SOLES){
                this.#total_soles += itemRow.subtotal
            }
            if (itemRow.currency === EURO){
                this.#total_eur += itemRow.subtotal
            }
        })

        this.update_total()

    }

    update_total(){
        const total_soles_object = document.getElementById("total-amount-soles")
        const total_usd_object = document.getElementById("total-amount-usd")
        const total_euros_object = document.getElementById("total-amount-euros")
        total_soles_object.innerHTML = this.#total_soles.toFixed(2)
        total_usd_object.innerHTML = this.#total_usd.toFixed(2)
        total_euros_object.innerHTML = this.#total_eur.toFixed(2)

    }
}



document.addEventListener('DOMContentLoaded', function () {
    const mySelect = document.getElementById('id_supplier');

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
                    const itemRows = document.querySelectorAll('.item-row')
                    const itemRowManager = new ItemListManager(itemRows)
                    /*const selectors = document.querySelectorAll('.supplier-product-selector');

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
                                    price_input.value = data.price
                                    currency_input.value = data.currency
                                    const itemRows = itemRowManager.itemRows
                                    itemRows[index].item = new Item(
                                        selectorChanged.value,
                                        data.price,
                                        data.currency,
                                        quantity_input.value,
                                    )
                                })

                        })
                    })*/

                })

        }
    })

})
