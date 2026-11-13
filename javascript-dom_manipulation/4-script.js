/* global document */
const addItem = document.querySelector('#add_item');
const list = document.querySelector('ul.my_list');

addItem.addEventListener('click', () => {
  const item = document.createElement('li');
  item.textContent = 'Item';
  list.appendChild(item);
});
