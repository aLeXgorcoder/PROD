// Функция для проверки, видим ли элемент на экране
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return rect.top >= 0 && rect.bottom <= window.innerHeight;
}

// Функция для добавления класса "visible" элементам, которые видны на экране
function checkVisibility() {
    const elements = document.querySelectorAll('.info__content');

    elements.forEach((element) => {
        if (isInViewport(element)) {
            element.classList.add('visible');
        }
    });
}

// Добавляем обработчик события прокрутки
window.addEventListener('scroll', checkVisibility);

// Выполняем проверку при загрузке страницы
document.addEventListener('DOMContentLoaded', checkVisibility);









