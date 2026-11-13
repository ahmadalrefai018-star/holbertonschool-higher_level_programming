/* global document */
const header = document.querySelector('header');
const toggleHeader = document.querySelector('#toggle_header');

toggleHeader.addEventListener('click', () => {
  header.className = header.classList.contains('red') ? 'green' : 'red';
});
