function openSignup() {
    blur()
    document.getElementById('signUpMenu').classList.remove('hidden')
}

function closeSignup() {
    console.log('test')
    blur()
    document.getElementById('signUpMenu').classList.add('hidden')
}

function openLogin() {
    blur()
    document.getElementById('loginMenu').classList.remove('hidden')
}

function closeLogin() {
    blur()
    document.getElementById('loginMenu').classList.add('hidden')
}

function blur() {
    document.getElementById('blur').classList.toggle('hidden')
}

async function getDistance(addr1, addr2) {
    addr1 = await fetch('/encode', {
        'method': 'POST',
        'body': JSON.stringify({'address': addr1})
    }).then(x => x.json())
    console.log(addr1)
    addr2 = await fetch('/encode', {
        'method': 'POST',
        'body': JSON.stringify({'address': addr2})
    }).then(x => x.json())
    console.log(addr2)
    let distance = await fetch(`https://api.distancematrix.ai/maps/api/distancematrix/json?origins=${addr1}&destinations=${addr2}&key=4hh2rHrfull5R0Pl2CRgsrM4DPI0a`)
    .then(x => x.json())
    console.log(distance)
    console.log(distance['rows'])
    console.log(distance['rows'][0])
    console.log(distance['rows'][0]['elements'])
    console.log(distance['rows'][0]['elements'][0])
    console.log(distance['rows'][0]['elements'][0]['distance'])
    console.log(JSON.stringify(distance['rows'][0]['elements'][0]['origin']))
    console.log(JSON.stringify(distance['rows'][0]['elements'][0]['destination']))
}

var requestOptions = {
    method: 'GET',
  };
  
  fetch("https://api.geoapify.com/v1/geocode/search?text=980%20Camino%20Verde%20Circle%2C%20Walnut%20Creek%2C%20CA%2094597%2C%20United%20States&apiKey=940b1c6bcc924f6ba1e6e07f6cc0fab5", requestOptions)
    .then(response => response.json())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));