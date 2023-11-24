// Ожидание загрузки страницы
window.addEventListener('DOMContentLoaded', () => {
  // Отправка запроса на выполнение скрипта
  fetch('/run-script?chart=1')
    .then(response => response.text())
    .then(data => {
      // Создание нового элемента img и установка данных изображения в качестве источника
      var img = document.createElement('img');
      img.src = "data:image/png;base64," + data;

      // Добавление элемента img на страницу
      var chartContainer = document.getElementById('chart-container1');
      chartContainer.appendChild(img);
    })
    .catch(error => {
      // Обработка ошибок выполнения запроса или скрипта
      console.error('Ошибка выполнения запроса:', error);
      alert('Ошибка выполнения запроса.');
    });
});
