from django.db import migrations


def forwards_func(apps, schema_editor):
    News = apps.get_model("mainapp", "News")
    News.objects.create(
        title="Запуск нового курса по Python",
        preambule="Мы рады Вам сообщить о запуске нового курса по Python для \
            начинающих!",
        body="Python предназначен для разработки и изучения новых приложений. \
            Мы предлагаем не просто изучить новый язык программирования, но и \
            научиться применять его на практике. Данный курс будет полезен не \
            только тем, кто хочет научиться программировать, но и всем тем, \
            кому не хватает времени на выполнение домашних заданий, а также \
            тем, у кого нет возможности посещать курсы. Курс состоит из 7 \
            встреч (одно занятие в неделю длительностью 3 часа).\r\nВстречи \
            проводятся по воскресеньям с 14:00.",
    )
    News.objects.create(
        title="Урока по PHP в среду не состоится",
        preambule="Всем, кто не успел купить курс в понедельник, настоятельно \
            рекомендую это сделать по ссылке в конце публикации.",
        body="Сегодня в Саратове не будет проходить открытый урок по PHP, \
            который должен был состояться в среду на факультете компьютерных \
            наук СГУ. Преподавательница, за которой закреплена аудитория, \
            сказала что заболела и не придет. На следующий урок, \
            запланированный на 28 февраля, перенесли все, кроме курса \
            «Веб-программирование». Об этом сообщили в группе факультета в \
            социальной сети «Вконтакте». Курс «Веб-программист» состоит из \
            двух частей. Первая — общий курс в течение 72 часов.",
    )
    News.objects.create(
        title="Всем руководителям подразделений подключится к Zoom",
        preambule="Все сотрудники подключены к Zoom, поэтому мы видим, что \
            они делают и что говорят.",
        body="Каждый из 5 руководителей будет в одном из своих офисов с \
            помощью этого приложения, мы хотим, чтобы они могли видеть все, \
            что происходит на сайте, просматривать отчеты, которые мы им \
            предоставляем. После того, как сотрудники подключили ZOOM, нам \
            необходимо, чтобы каждый секретарь, менеджер и т. Д. Были \
            подключены к каждому из этих 5 компьютеров.",
    )
    News.objects.create(
        title="Сегодня студенты всего мира отмечают праздник",
        preambule="Подробности внутри...",
        body="Сегодня студенты всего мира отмечают праздник, который \
            официально является международным, но более распространен в \
            азиатских странах, таких как Китай или Япония. Он называется \
            Фестиваль студенческого пирога (Holly Fest) и празднуется каждый \
            год в начале сентября. Это праздник, объединяющий студентов во \
            всем мире, которые отмечают начало нового учебного года и дарят \
            друг другу подарки. Во многих азиатских странах этот день также \
            знаменует начало нового года по китайскому календарю День \
            Рождения: 9 июля, 23 года",
    )
    News.objects.create(
        title="Встречайте нового преподавателя направления DevOps",
        preambule="Дмитрий Шишмарев работает в IT-бизнесе с 2001 года.",
        body="До прихода в компанию 1С-Битрикс начинал карьеру в качестве \
            системного администратора. В 2009 перешел на должность \
            DevOps-инженера, где и трудится по сей день, развиваясь в своей \
            сфере. Дмитрий является сертифицированным специалистом компании \
            Bitrix. На его счету более 30 успешно реализованных проектов, \
            среди которых: разработка корпоративной системы управления \
            веб-проектами на базе 1C-Bitrix",
    )
    News.objects.create(
        title="JavaScript снова возглавил рейтинг самых отвратительных \
            языков",
        preambule="И опять, и снова.",
        body="Рейтинг самых отвратительных языков программирования, \
            составленный британским изданием, возглавляет JavaScript. В опросе \
            приняли участие более 1000 специалистов по разработке ПО, \
            работающих в различных компаниях. При составлении списка \
            учитывались такие свойства языка, как сложность и простота \
            обучения, а также производительность. Специалисты оценивали язык \
            по 10-балльной шкале, где один балл означал «ужасающий», а 10 \
            баллов – «отвратительный».",
    )


def reverse_func(apps, schema_editor):
    News = apps.get_model("mainapp", "News")
    News.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]