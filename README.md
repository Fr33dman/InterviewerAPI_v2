# Setup
1. Clone this repo to your computer
2. Print this in ur console
```
docker-compose up --build --detach
```
# API

## Authentication
``/token/``

User = "admin"

password = "password"

## Refresh authentication token
``/token/refresh/``

## Interviews endpoint
General information about interview

### URL
``/interview/{pk}``

#### Fields
|Field          |Type      | Description                                                                                |
|---------------|----------|--------------------------------------------------------------------------------------------|
|name           | string   | name of interview                                                                          |
|start_time     | datetime | example : "2021-05-14 16:32:56", time when interview starts                                |
|end_time       | datetime | example : "2021-05-14 16:32:56", time when interview ends                                  |
|description    | string   | description of interview                                                                   |
|question       | dict     | question fields                                                                            |

#### Create

same like an answer but without id's, the only thing you should know,
that OA and MA types requires possible answers

example:

```json
{
    "name": "Опрос кандидата о приеме на работу",
    "start_time": "2021-11-02T12:00:00Z",
    "end_time": "2021-11-05T12:00:00Z",
    "description": "Расскажите о себе",
    "questions": [
        {
            "text": "Как вас зовут?",
            "type": "TA"
        },
        {
            "text": "Укажите свой пол",
            "type": "OA",
            "possible_answers": [
                {
                    "text": "Мужчина"
                },
                {
                    "text": "Женщина"
                }
            ]
        },
        {
            "text": "Сколько вы хотите зарабатывать?",
            "type": "OA",
            "possible_answers": [
                {
                    "text": "Меньше 50 тыс. рублей"
                },
                {
                    "text": "От 50 до 100 тыс. рублей"
                },
                {
                    "text": "Более 100 тыс. рублей"
                }
            ]
        },
        {
            "text": "Сколько времени вы хотите уделять работе?",
            "type": "TA"
        },
        {
            "text": "Укажите свой стаж работы",
            "type": "TA"
        },
        {
            "text": "В какие настольные игры вы играете?",
            "type": "MA",
            "possible_answers": [
                {
                    "text": "Шахматы"
                },
                {
                    "text": "Карты"
                },
                {
                    "text": "Мафия"
                },
                {
                    "text": "Поккер"
                },
                {
                    "text": "Другое"
                }
            ]
        }
    ]
}
```

### Question
Questions in each interview

Question can be one of 3 types:
- Text answer (TA)
- One answer (OA)
- Many answers (MA)

#### Fields
|Field          |Type      | Description                                                                                |
|---------------|----------|--------------------------------------------------------------------------------------------|
|interview      | int      | id of interview                                                                            |
|text           | string   | text of question                                                                           |
|type           | string   | one of types "TA" / "OA" / "MA"                                                            |

### Possible answer
Possible answers that user can choose if question type is "One answer" or "Many answers"

#### Fields
|Field          |Type      | Description                                                                                |
|---------------|----------|--------------------------------------------------------------------------------------------|
|question       | int      | id of question                                                                             |
|text           | string   | text of possible answer                                                                    |

### Answer endpoint
User's answer on each question

#### URL
``/answer/{pk}/?interview={int}``

#### Fields
|Field          |Type      | Description                                                                                |
|---------------|----------|--------------------------------------------------------------------------------------------|
|user           | int      | id of user                                                                                 |
|interview      | int      | id of interview                                                                            |
|question       | int      | id of question                                                                             |
|answer         | int      | id of answer if question type is "One answer" or "Many answers"                            |
|text_answer    | string   | answer text if question type is "Text answer"                                              |

#### Create
You can create one answer or list of answers, but in fields interview,
question you need to put id of them, and in field answer you put
list of id's

example:

```json
[
    {
        "interview": 1,
        "text_answer": "Григорий",
        "question": 1
    },
    {
        "interview": 1,
        "answer": [1],
        "question": 2
    },
    {
        "interview": 1,
        "answer": [4],
        "question": 3
    },
    {
        "interview": 1,
        "text_answer": "МНОГО! ЛЮБЛЮ СВОЮ РАБОТУ! Я НЕ ЛОДЫРЬ",
        "question": 4
    },
    {
        "interview": 1,
        "text_answer": "8 месяцев",
        "question": 5
    },
    {
        "interview": 1,
        "answer": [6, 7, 8],
        "question": 6
    }
]
```