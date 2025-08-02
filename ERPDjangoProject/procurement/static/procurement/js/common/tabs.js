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

document.querySelectorAll('.tab-button.active').forEach(
    tab => {
        document.getElementById(tab.getAttribute('data-tab')).classList.add('active')
    }
)
