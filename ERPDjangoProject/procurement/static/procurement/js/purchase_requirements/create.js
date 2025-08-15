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
    #deleteButton = null
    #supplierProductSelectorChangedEvents = []
    #rowDeleteEvents = []


    constructor(rowNode){
        this.#rowNode = rowNode
        this.#subtotalNode = this.#rowNode.querySelector('.subtotal')
        this.#priceNode = this.#rowNode.querySelector('.price-field')
        this.#currencyNode = this.#rowNode.querySelector('.currency-field')
        this.#quantityNode = this.#rowNode.querySelector('.quantity-field')
        this.#supplierProductSelectorNode = this.#rowNode.querySelector('.supplier-product-selector')
        this.#deleteButton = this.#rowNode.querySelector('.btn-remove-item')

        this.#deleteButton.addEventListener('click', () => {
            this.#rowNode.remove()
            console.log("delete button clicked")
            console.log(this.#rowNode)
            console.log(this.#rowDeleteEvents)
            this.#rowDeleteEvents.forEach(event => {
                event(this)
            })
        })

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

    addDeleteEvent(event){
        console.log("add delete event")
        console.log(event)
        console.log(this.#rowDeleteEvents)
        this.#rowDeleteEvents.push(event)
    }


    updateSubTotal(){
        this.#subtotalNode.innerHTML = this.subtotal.toFixed(2)
    }

    get node(){
        return this.#rowNode
    }

    setIndex(index){
        this.setIndexNode(this.#supplierProductSelectorNode, index, 'supplier?product')
        this.setIndexNode(this.#priceNode, index, 'price')
        this.setIndexNode(this.#currencyNode, index, 'currency')
        this.setIndexNode(this.#quantityNode, index, 'quantity')

    }

    setIndexNode(node, index, field){
        const attributes = {
            name: `items-${index}-${field}`,
            id: `id_items-${index}-${field}`
        }
        for  (const key in attributes ){
            node.setAttribute(key, attributes[key])
        }

    }

}

const products = []

class ItemListManager {
    #itemsBody = null
    #itemRows = []
    #total_soles = 0
    #total_usd = 0
    #total_eur = 0
    #selectedOptions = new Set()
    #addButton = null
    #formmanager = null
    constructor(itemsBody, addButton, formmanager){

        this.#formmanager = formmanager

        this.#itemsBody = itemsBody

        const itemRowsNodes = this.#itemsBody.querySelectorAll('.item-row')

        const nodes_array = Array.from(itemRowsNodes)

        this.#itemRows = nodes_array.map(itemRowNode => new ItemRow(itemRowNode))
        this.#itemRows.forEach(itemRow => {
            this.addEventsToItemRow(itemRow)
        })

        this.#addButton = addButton
        this.#addButton.addEventListener('click', () => {
            this.addItemRow()
        })

    }

    addEventsToItemRow(itemRow){
            itemRow.addSupplierProductSelectorChangedEvent(this.compute_totals.bind(this))
            itemRow.addSupplierProductSelectorChangedEvent(this.optionsUsedUpdate.bind(this, itemRow.supplierProductSelectorNode))
            itemRow.addDeleteEvent(this.removeItemRow.bind(this))
    }

    optionsUsedUpdate(selectorChanged){
        console.log("options used update")
        const selectedValues = new Set()
        this.#itemRows.forEach(itemRow => {
            console.log("item row selected values")
            console.log(itemRow.item)
            if (itemRow.supplierProductSelectorNode.value !== ""){
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



    addItemRow(){
        const itemNode = this.#itemRows[0].node.cloneNode(true)
        this.#itemsBody.appendChild(itemNode)
        const itemRow = new ItemRow(itemNode)
        this.#itemRows.push(itemRow)
        this.addEventsToItemRow(itemRow)

        this.reorder()
    }

    reorder(){
        this.#itemRows.forEach((itemRow, index) => {
            itemRow.setIndex(index)
        })
    }

    removeItemRow(itemRow){
        console.log("before remove item row")
        console.log(this.#itemRows.length)
        console.log(itemRow)
        this.#itemRows.splice(this.#itemRows.indexOf(itemRow), 1)

        console.log("after item row")
        console.log(this.#itemRows.length)
        this.reorder()
        this.compute_totals()

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
                    const addButton = document.getElementById('add-item')
                    const itemsBody = document.getElementById('items-tbody')
                    console.log(itemsBody)
                    const itemRowManager = new ItemListManager(itemsBody, addButton)

                })

        }
    })

})
