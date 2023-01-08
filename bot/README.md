Telegram Bot to use custom api 
---

which scrapes data from hookah crm and stores collected data in the database

---- 

- [ ] Greetings message on `\start` and `\help` 

- [ ] Request sales data
    - for one month
    - for specified period of time 
    *optionally:* 
        - get sales predictions 
        - send data in image graph format

- [ ] Add inline keyboard for every keyboard
  - [ ] for `\sales_month` "в excel"

- [ ] Add menu as **BotFather**

---- 
#### Example of how to use this bot 

> `/start` 

> Привет! Этот бот создан для получения данных с сайта hookah crm 
>
> *Доступные команды:*  
> /credentials — ввести пароль и email от hookah.work
> /help — справка *(информация о боте)*

> `/credentials`

> Введите email

> email@example.com

> Введите пароль

> secret_password

> Данные успешно сохранены
> email: eamil@example.com
> пароль: secret_password

*(две inline кнопки: `продолжить` `изменить данные`)*

> нажать `продолжить`

> Теперь выберете команду!

*(inline кнопки: `получить данные о продажах` `вернуться обратно`)*

> `Получить данные о продажах`

> Выберете следующее действие:
*(inline кнопки: `обновить` `получить данные`)*