# Группа №3
## Архитектура проекта

![Архитектура проекта](img/ar_project.png)

Разработчики модулей программы:
* GUI - Александр
* Model - Рафаэль
* Логирование - Артем
* Main - Артем
 
### **main_calculation(expression) -> str**  
на вход получает строку, которую надо вычислить
возвращает итог типа str
например:  
result = main_calculation('(2*3-1)*(1+2)/(3*(8/2+1))'  
возвращает '1.0'

### **log**
Модуль log принимает данные от модулей calc и main и на основе этих данных создает запись о выполняемых программой 
действиях в файле с расширением csv. <br>
Формат записи: *дата; время; операция; пользователь;* <br>
если выполнялись вычисления, то добавляются следующие записи: *условие; результат*

### **gui**
Модуль gui представляет собой графический интерфейс взаимодействия с пользователем. Пользователь вводит посредством 
клавиатуры или панели программы данные для вычисления, эти данные отображаются в поле дисплея и 
передаются в модуль calc для дальнейшей обработки, от модуля calc получает результат вычисления и выводит обратно на 
дисплей.

### **main**
Модуль main является точкой входа. С его помощью происходит запуск остальных модулей программы.

### **Пример использования программы**
Запуск программы:

![Запуск программы](img/start.jpg)

Задание условия для вычисления:

![Вычисление](img/1.jpg)

Решение:

![Решение](img/2.jpg)
