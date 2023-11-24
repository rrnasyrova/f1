const scriptURL = 'https://script.google.com/macros/s/AKfycby5sIOZz_Ookt1uOdQI10fGQCQYxGfuD0s_iF4PbRmFQiquHDkOxl8YTlkNQrOyMr1d/exec'
const form = document.forms['submit-to-google-sheet']
const sendText = document.getElementById('sendText')

form.addEventListener('submit', e => {
  e.preventDefault()
  fetch(scriptURL, { method: 'POST', body: new FormData(form)})
    .then(response => {
        sendText.innerHTML = 'Спасибо, ваши данные отправлены успешно!'
        setTimeout(function(){
            sendText.innerHTML = ''
        }, 3000)
        form.reset()
    })
    .catch(error => console.error('Error!', error.message))
})