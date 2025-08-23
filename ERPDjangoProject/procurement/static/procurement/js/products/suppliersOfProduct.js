class SuppliersOfProduct{
    #rowNode = null
    constructor(row){
        this.#rowNode = row
        this.supplier = this.#rowNode.querySelector('.supplier-field')
        this.price = this.#rowNode.querySelector('.price-field')
        this.currency = this.#rowNode.querySelector('.currency-field')
        this.unit_of_measure = this.#rowNode.querySelector('.unit-of-measure-field')

    }
}

class SuppliersOfProductNew{

}

class SuppliersOfProductListManager{
    #suppliersOfProductList = []
    #suppliersOfProductListNew = []
    #tableBody = null
    #tableBodyNew = null
    constructor(tablebody, tablebodynew, manager){
        const rows = tablebody.querySelectorAll('.supplier-product')
        const rows_new = tablebodynew.querySelectorAll('.supplier-product-new')
        const nodes_array = Array.from(rows)
        nodes_array.forEach(row => {
            this.#suppliersOfProductList.push(new SuppliersOfProduct(row))
        })
        const node_new_array = Array.from(rows_new)
        nodes_array.forEach(row =>{
            this.#suppliersOfProductListNew.push(new SuppliersOfProductNew(row))
        })

    }
}