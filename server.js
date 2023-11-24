const express = require('express');
const app = express();
const path = require('path');
const { exec } = require('child_process');

// Отправка статических файлов из папки public
app.use(express.static(path.join(__dirname, 'public')));

// Обработка запросов на главную страницу
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public/html/index.html'));
});

app.get('/run-script', (req, res) => {
  const chart = req.query.chart; // Получаем номер графика из запроса

  // Строим путь к файлу Python-скрипта на основе номера графика
  const pythonScriptPath = `/Users/reginanasyrova/Desktop/f1/data_plot${chart}.py`;

  exec(`python ${pythonScriptPath}`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Ошибка выполнения скрипта: ${error}`);
      res.status(500).send('Ошибка выполнения скрипта.');
    } else {
      // Отправляем результат выполнения скрипта в качестве ответа
      res.send(stdout);
    }
  });
});

// Запуск сервера
app.listen(3000, () => {
  console.log('Сервер запущен на порту 3000.');
});
