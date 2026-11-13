/* global document, fetch */
fetch('https://swapi-api.hbtn.io/api/people/5/?format=json')
  .then(response => response.json())
  .then(character => {
    document.querySelector('#character').textContent = character.name;
  });
