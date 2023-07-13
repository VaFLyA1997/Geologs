document.addEventListener('DOMContentLoaded', () => {
    const burgerBar = document.querySelector('.burger__bar')
    const headerNav = document.querySelector('.header__nav')
    const burgerBtn = document.querySelector('.burger')
    const profileBtn = document.querySelector('.header__profile-link')
    const popup = document.querySelector('.popup')
    const popupCloseBtn = document.querySelector('.popup__close')
  
    burgerBtn.addEventListener('mousedown', () => {
      headerNav.classList.toggle('header__nav--open')
      burgerBar.classList.toggle('burger__bar--close')
    })
  
    profileBtn.addEventListener('mousedown', () => {
      popup.classList.add('popup--opened')
    })
  
    popupCloseBtn.addEventListener('mousedown', () => {
      popup.classList.remove('popup--opened')
    })
  
  })


// var loginForm = document.getElementById('login-form');

// loginForm.addEventListener('submit', function(e) {
//     e.preventDefault(); // Отменяем стандартное поведение отправки формы

//     // Создаем объект FormData для сбора данных из формы
//     var formData = new FormData(loginForm);

//     // Создаем AJAX запрос к серверу
//     var xhr = new XMLHttpRequest();
//     xhr.open('POST', '/login_ajax/', true);
//     xhr.onreadystatechange = function() {
//         if (xhr.readyState === XMLHttpRequest.DONE) {
//             if (xhr.status === 200) {
//                 // Обработка успешного ответа от сервера
//                 var response = JSON.parse(xhr.responseText);
//                 if (response.status === 'success') {
//                     // Добавьте код для перехода на другую страницу или обновления текущей страницы
//                     window.location.href = '/profile/';
//                 } else {
//                     alert('Ошибка авторизации: ' + response.message);
//                 }
//             } else {
//                 // Обработка ошибочного ответа от сервера
//                 alert('Ошибка при отправке AJAX запроса');
//             }
//         }
//     };
//     xhr.send(formData);
// });