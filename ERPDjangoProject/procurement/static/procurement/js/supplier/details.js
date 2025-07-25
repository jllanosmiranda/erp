export function openTab(event, tabName){
    const tabs = document.querySelectorAll('.tabcontent');
    tabs.forEach(tab => {
        tab.classList.remove('active')
    })

    const active_tab = document.getElementById(tabName);
    active_tab.classList.add('active');
}

function activeTab (clicked_tab){
   const all_tabs = document.querySelectorAll('.tab-button')
    all_tabs.forEach(tab => {
        tab.classList.remove('active')
    })
    clicked_tab.classList.add('active')
}

document.querySelectorAll('.tab-button').forEach(
    btn => {
        btn.addEventListener('click', function(event){
            openTab(event, btn.getAttribute('data-tab'))
            activeTab(btn)
            console.log(btn.getAttribute('data-tab'))
        })
    }
)

function cleanClonedForm(clone_node){
    const inputs = clone_node.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        console.log(input.type)
        switch (input.type){
            case 'checkbox':
            case 'radio':
                input.checked = false;
                break;
            default:
                console.log("inside default")
                input.value = '';
                console.log('new value')
                console.log(input.value)
        }
    })
}

export function AddFormSet(event, list_id, prefix){
    var contactlist = document.getElementById(list_id)
    var total_forms = document.getElementById(`id_${prefix}-TOTAL_FORMS`)
    var currentFormCount = contactlist.getElementsByClassName('dynamic-form').length
    var new_form = contactlist.getElementsByClassName('dynamic-form')[0].cloneNode(true)

    cleanClonedForm(new_form)

    console.log("new forma data clean")
    const inputs = new_form.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        console.log(input.type)
                console.log('value')
                console.log(input.value)
        })

    var formExp = RegExp(`${prefix}-0-`,'g')

    new_form.innerHTML = new_form.innerHTML.replace(formExp, `${prefix}-${currentFormCount}-`)

    console.log("new forma data clean")
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


document.querySelectorAll('.add-form-btn').forEach(
    btn => {
        btn.addEventListener('click', function(event){
            event.preventDefault()
            AddFormSet(event, btn.getAttribute('data-list-id'), btn.getAttribute('data-list-prefix'))
            console.log(btn.getAttribute('data-list-id'))
        })
    }
)

document.querySelectorAll('.remove-form-btn').forEach(
    btn => {
        btn.addEventListener('click', function(event){
            event.preventDefault()
            RemoveFormSet(event,
                btn.getAttribute('data-list-id'),
                btn.getAttribute('data-list-prefix'))
            console.log(btn.getAttribute('data-list-id'))
        })
    }
)
