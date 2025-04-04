
function myFunction(){
   alert('Button was clicked')
}

function otherFunction(){
   body = document.getElementById('list-elements')
   newElement = document.createElement('div')
   newElement.innerHTML = '<p>some text</p>'
   newElement.setAttribute("class", "dummy")
   body.insertAdjacentElement('beforeend', newElement)
}

function removeElement(){
   body = document.getElementById('list-elements')
   elements = document.getElementsByClassName('dummy')
   if (elements.length > 0){
      body.removeChild(elements[elements.length - 1])
   }

}