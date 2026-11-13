/* global document */
const header = document.querySelector('header');
const redHeader = document.querySelector('#red_header');

redHeader.addEventListener('click', () => {
  header.style.color = '#FF0000';
});
