/* global document, fetch */
const listMovies = document.querySelector('#list_movies');

fetch('https://swapi-api.hbtn.io/api/films/?format=json')
  .then(response => response.json())
  .then(data => {
    data.results.forEach(movie => {
      const item = document.createElement('li');
      item.textContent = movie.title;
      listMovies.appendChild(item);
    });
  });
