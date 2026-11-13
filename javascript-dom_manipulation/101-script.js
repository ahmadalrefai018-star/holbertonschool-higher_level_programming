/* global document, fetch */
document.addEventListener('DOMContentLoaded', () => {
  const languageCode = document.querySelector('#language_code');
  const hello = document.querySelector('#hello');

  document.querySelector('#btn_translate').addEventListener('click', () => {
    fetch('https://hellosalut.stefanbohacek.com/?lang=' + encodeURIComponent(languageCode.value))
      .then(response => response.json())
      .then(data => {
        hello.textContent = data.hello;
      });
  });
});
