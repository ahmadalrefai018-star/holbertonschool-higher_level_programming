/* global document */
document.addEventListener('DOMContentLoaded', () => {
  const list = document.querySelector('#my_list') || document.querySelector('ul.my_list');

  document.querySelector('#add_item').addEventListener('click', () => {
    const item = document.createElement('li');
    item.textContent = 'Item';
    list.appendChild(item);
  });

  document.querySelector('#remove_item').addEventListener('click', () => {
    const lastItem = list.lastElementChild;
    if (lastItem) {
      lastItem.remove();
    }
  });

  document.querySelector('#clear_list').addEventListener('click', () => {
    list.textContent = '';
  });
});
