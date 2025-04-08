import {ActiveSubNav} from "/static/nav/js/navigation.js"

document.addEventListener('DOMContentLoaded', () => {
    ActiveSubNav('suppliers')
})

export function openTab(event, tabName){
    var tabcontent = document.getElementsByClassName('tabcontent');
    for (let i = 0; i < tabcontent.length; i++){
        tabcontent[i].style.display = 'none';
    }

    document.getElementById(tabName).style.display = 'block';
}

export function AddFormSet(event, list_id, prefix){
    var contactlist = document.getElementById(list_id)
    var total_forms = document.getElementById(`id_${prefix}-TOTAL_FORMS`)
    var currentFormCount = contactlist.getElementsByClassName('dynamic-form').length
    var new_form = contactlist.getElementsByClassName('dynamic-form')[0].cloneNode(true)

    var formExp = RegExp(`${prefix}-0-`,'g')

    new_form.innerHTML = new_form.innerHTML.replace(formExp, `${prefix}-${currentFormCount}-`)
    contactlist.appendChild(new_form)
    total_forms.setAttribute('value', currentFormCount + 1)
}

export function RemoveFormSet(event, list_id, prefix){
    var contactlist = document.getElementById(list_id)
    var totalforms = document.getElementById(`id_${prefix}-TOTAL_FORMS`)
    var currentFormCount = contactlist.getElementsByClassName('dynamic-form').length

    if (currentFormCount > 1){
        var all_forms = contactlist.getElementsByClassName("dynamic-form")
        var last_form = all_forms[all_forms.length - 1]
        contactlist.removeChild(last_form)
        totalforms.setAttribute('value', currentFormCount - 1)

    }

}
