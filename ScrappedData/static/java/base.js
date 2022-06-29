ad = document.getElementsByName('name')

function UpdateCost() {
    checked_a = []
    var download_value = ''
    for (let i = 0; i < ad.length; i++) {
        if (ad[i].checked) {
            checked_a.push(ad[i].value)
            id = ad[i].value
            title = document.getElementById(id).innerHTML.trim()
            console.log(title)
            if (download_value === '') {
                download_value = id+'-'+title
            } else {
                download_value = download_value + " &&&& " + id + '-' + title
            }
        }
        if (download_value != '') {
            input_section = document.getElementById('download_id')
            console.log(input_section)
            input_section.classList.remove('disappear')
            document.getElementById('input_box').value = download_value
        } else {
            input_section = document.getElementById('download_id')
            console.log(input_section)
            input_section.classList.add('disappear')
        }
        
    }
    console.log(download_value)
}

window.onchange = UpdateCost




flogin_button = document.getElementById('login_flipkart')
flogin_button.addEventListener('click', () => {
    fmodal = document.getElementById('fmodalid')
    if (fmodal.style.display === 'none') {
        fmodal.style.display = 'block'
    } else {
        fmodal.style.display = "none"
    }
})

alogin_button = document.getElementById('login_amazon')
alogin_button.addEventListener('click', () => {
    amodal = document.getElementById('amodalid')
    if (amodal.style.display === 'none') {
        amodal.style.display = 'block'
    } else {
        amodal.style.display = "none"
    }
})










var modal = document.getElementsByName("modal_box");



// Get the button that opens the modal
var btn = document.getElementsByName("modal_button");
console.log(btn[0])

btn = document.getElementById('myBtn')
btn.addEventListener('click', () => {
    console.log('inside the function')
})


// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function () {
    console.log('inside the function')
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}