#!/usr/bin/env python3
"""Generate the complete static Vitcleaner site.

The checked-in HTML is production output. Set SITE_URL before running this file
when the project moves to a custom domain, for example:
SITE_URL=https://example.by python scripts/build.py
"""

from html import escape as E
from pathlib import Path
from urllib.parse import urlsplit
from xml.sax.saxutils import escape as X
import json
import os

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get(
    "SITE_URL", "https://yaroslavkiri4ykknifhit-max.github.io/cleaner/"
).rstrip("/") + "/"
PHONE = "+375295973713"
PHONE_DISPLAY = "+375 (29) 597-37-13"
VIBER = "https://viber.click/375295973713"
LASTMOD = "2026-10-21"
METRIKA_ID = 113723408
METRIKA_SCRIPT = f'''<!-- Yandex.Metrika counter -->
<script type="text/javascript">
    (function(m,e,t,r,i,k,a){{
        m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};
        m[i].l=1*new Date();
        for (var j = 0; j < document.scripts.length; j++) {{if (document.scripts[j].src === r) {{ return; }}}}
        k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
    }})(window, document,'script','https://mc.yandex.ru/metrika/tag.js?id={METRIKA_ID}', 'ym');

    ym({METRIKA_ID}, 'init', {{ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true}});
</script>
<!-- /Yandex.Metrika counter -->'''
METRIKA_NOSCRIPT = f'''<!-- Yandex.Metrika counter -->
<noscript><div><img src="https://mc.yandex.ru/watch/{METRIKA_ID}" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
<!-- /Yandex.Metrika counter -->'''

ICONS = {
    "spark": '<path d="m12 3 2.5 6.5L21 12l-6.5 2.5L12 21l-2.5-6.5L3 12l6.5-2.5L12 3Z"/><path d="m20 2 .6 1.4L22 4l-1.4.6L20 6l-.6-1.4L18 4l1.4-.6Z"/>',
    "arrow": '<path d="M4 12h15m-6-6 6 6-6 6"/>',
    "pin": '<path d="M19 10c0 5-7 11-7 11S5 15 5 10a7 7 0 1 1 14 0Z"/><circle cx="12" cy="10" r="2.5"/>',
    "check": '<path d="m5 12 4 4 10-10"/>',
    "shield": '<path d="m12 3 8 3v6c0 5-8 9-8 9s-8-4-8-9V6l8-3Z"/><path d="m8 12 3 3 5-6"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "phone": '<path d="m6 3 4 4-2 3c2 3 3 4 6 6l3-2 4 4-2 3C11 22 2 13 3 5l3-2Z"/>',
    "chat": '<path d="M21 11a9 9 0 0 1-9 9 10 10 0 0 1-4-.8L3 21l1.7-5A9 9 0 1 1 21 11Z"/><path d="M8 11h8M8 8h5"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "wallet": '<rect x="3" y="5" width="18" height="15" rx="3"/><path d="M3 9h18m-5 4h5v4h-5Z"/>',
    "fabric": '<path d="M4 4h16v16H4ZM4 9h16M4 15h16M9 4v16M15 4v16"/>',
    "photo": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="m3 16 5-5 4 4 3-3 6 6"/><circle cx="16" cy="8" r="1"/>',
}


def icon(name):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


SERVICES = [
    {
        "slug": "himchistka-mebeli",
        "short": "Мягкая мебель",
        "card": "Химчистка мебели",
        "title": "Химчистка мягкой мебели в Витебске на дому",
        "description": "Профессиональная химчистка мягкой мебели на дому в Витебске и области: диваны, кресла, стулья и матрасы. Оценка по фото, реальные работы до и после.",
        "lead": "Чистим тканевую обивку диванов, кресел, стульев и матрасов с выездом. Перед работой оцениваем материал, загрязнения и заранее обсуждаем ожидаемый результат.",
        "keywords": "диваны, кресла, стулья, матрасы",
        "sections": [
            ("Что можно почистить на дому", "Работаем с прямыми и угловыми диванами, креслами, обитыми тканью стульями, изголовьями кроватей и матрасами. Для кожаной мебели используем отдельный подход. Перед записью попросим общий снимок и крупные фото загрязнений."),
            ("Как проходит профессиональная чистка", "Осматриваем изделие, определяем тип обивки и проверяем реакцию материала на незаметном участке. Затем обрабатываем пятна, очищаем поверхность и извлекаем рабочий раствор вместе с загрязнениями. Метод и интенсивность обработки зависят от ткани."),
            ("Пятна, запахи и ограничения", "Свежие загрязнения обычно поддаются лучше старых. Результат зависит от происхождения пятна, предыдущих бытовых средств и состояния красителя. Выгорание, потёртости, разрывы и физический износ химчистка не устраняет — такие ограничения обсуждаем заранее."),
            ("Подготовка и высыхание", "Освободите доступ к мебели и уберите вещи с поверхности. Для работы понадобятся вода и электричество. После влажной чистки изделие должно полностью высохнуть; срок зависит от наполнителя, температуры и вентиляции."),
        ],
    },
    {
        "slug": "himchistka-divanov",
        "short": "Диваны",
        "card": "Химчистка диванов",
        "title": "Химчистка диванов на дому в Витебске",
        "description": "Химчистка прямых и угловых диванов на дому в Витебске и Витебской области. Удаление бытовых загрязнений и запахов, оценка стоимости по фото.",
        "lead": "Чистим прямые и угловые диваны без перевозки. Оцениваем ткань, пятна и объём работы по фотографиям, а цену согласуем до приезда.",
        "keywords": "прямые и угловые диваны",
        "sections": [
            ("Какие диваны чистим", "Работаем с прямыми, угловыми и модульными диванами, спальными местами, подушками и подлокотниками. Для точной оценки сообщите размер, материал, если он известен, и пришлите общий вид изделия."),
            ("От чего очищаем обивку", "Обрабатываем повседневную пыль, засаленные зоны, следы напитков, еды и другие бытовые загрязнения. Возможность убрать конкретное пятно или запах оценивается индивидуально: давность и предыдущая обработка сильно влияют на результат."),
            ("Как проходит чистка дивана", "После осмотра подбираем состав и тестируем его на малозаметном участке. Последовательно обрабатываем проблемные зоны, очищаем обивку и удаляем влагу экстрактором. Съёмные подушки и спальное место включаем в расчёт отдельно, если это требуется."),
            ("Когда диваном можно пользоваться", "После работы обивке нужно просохнуть. Не накрывайте диван и обеспечьте проветривание. Точное время зависит от ткани, наполнителя и условий в помещении; мастер даст ориентир после чистки."),
        ],
    },
    {
        "slug": "himchistka-matrasov",
        "short": "Матрасы",
        "card": "Химчистка матрасов",
        "title": "Химчистка матрасов в Витебске на дому",
        "description": "Химчистка матрасов на дому в Витебске: односторонняя и двусторонняя обработка, пятна и запахи. Расчёт по размеру и фотографиям.",
        "lead": "Очищаем поверхность матрасов на дому. Стороны, размер, пятна и необходимость обработки запаха согласуем по фото до начала работы.",
        "keywords": "односпальные и двуспальные матрасы",
        "sections": [
            ("Что входит в химчистку матраса", "Обрабатываем доступную поверхность, кант и боковые части. Односторонняя и двусторонняя чистка рассчитываются отдельно. Сообщите размер матраса и покажите пятна при дневном свете."),
            ("Что влияет на результат", "Белковые и старые органические загрязнения могут менять структуру и цвет ткани. Чем раньше начата профессиональная обработка и чем меньше бытовой химии использовалось до неё, тем выше шанс заметного результата."),
            ("Безопасный подход к материалу", "Перед основной работой проверяем ткань и подбираем допустимую влажность. Матрас нельзя переувлажнять: качественное извлечение раствора и нормальная вентиляция важны не меньше самого средства."),
            ("Как подготовить место", "Снимите постельное бельё, обеспечьте доступ к матрасу с нужных сторон и возможность проветривания. Спать на нём можно только после полного высыхания."),
        ],
    },
    {
        "slug": "himchistka-kresel-stulev",
        "short": "Кресла и стулья",
        "card": "Кресла и стулья",
        "title": "Химчистка кресел и стульев в Витебске",
        "description": "Химчистка мягких кресел, офисных и обеденных стульев в Витебске и области. Выезд на дом или в офис, расчёт по количеству и фото.",
        "lead": "Чистим мягкие кресла, офисные и обеденные стулья. Можно заказать одно изделие или сразу комплект для дома, офиса, кафе и другого помещения.",
        "keywords": "мягкие, офисные и обеденные кресла и стулья",
        "sections": [
            ("Какие изделия принимаем в работу", "Чистим тканевые кресла, мягкие обеденные стулья, офисные кресла и отдельные элементы мебели. Для расчёта нужны количество, общий вид и фото самых загрязнённых мест."),
            ("Чистка комплектом", "Если требуется обработать несколько одинаковых стульев, сообщите точное количество. Так проще заранее оценить время, расход материалов и согласовать общую стоимость без сюрпризов."),
            ("Особенности офисной мебели", "У офисных кресел учитываем сетчатые вставки, пластик, механизмы и состояние наполнителя. Работы можно согласовать на удобное время, чтобы меньше мешать работе помещения."),
            ("Пятна и время высыхания", "Пятна обрабатываются с учётом их происхождения и устойчивости ткани. После влажной чистки сиденья и спинки должны высохнуть при хорошей вентиляции."),
        ],
    },
    {
        "slug": "himchistka-kozhanoy-mebeli",
        "short": "Кожаная мебель",
        "card": "Кожаная мебель",
        "title": "Чистка кожаной мебели в Витебске",
        "description": "Профессиональная чистка кожаных диванов и кресел в Витебске. Оценка типа покрытия и состояния по фото, бережный уход без обещаний ремонта повреждений.",
        "lead": "Кожа и искусственные покрытия требуют иного ухода, чем ткань. Перед заказом оцениваем тип поверхности, загрязнения, трещины и потёртости.",
        "keywords": "кожаные диваны и кресла",
        "sections": [
            ("Почему коже нужен отдельный подход", "Средства для текстиля не подходят для кожаной поверхности. Сначала определяем вид покрытия и тестируем состав на малозаметном участке, чтобы не повредить цвет и защитный слой."),
            ("Что можно очистить", "Работаем с повседневными загрязнениями на сиденьях, спинках и подлокотниках. Возможность обработки сложных следов обсуждаем по крупным фотографиям до записи."),
            ("Чего чистка не исправит", "Трещины, облезшее покрытие, растянутые участки, глубокие царапины и потерю красителя нельзя убрать обычной чисткой. Это задачи ремонта или реставрации, и мы честно отделяем их от загрязнений."),
            ("Как получить расчёт", "Пришлите общий вид мебели, фото поверхности крупным планом и укажите количество посадочных мест. После оценки согласуем состав работ и стоимость."),
        ],
    },
    {
        "slug": "himchistka-kovrov",
        "short": "Ковры",
        "card": "Химчистка ковров",
        "title": "Химчистка ковров в Витебске",
        "description": "Химчистка ковров в Витебске и области: оценка состава, ворса и загрязнений, подбор подходящего способа, расчёт стоимости по размеру и фото.",
        "lead": "Очищаем ковры с учётом состава ворса и основания. До заказа оцениваем материал, размер, пятна и допустимый способ обработки.",
        "keywords": "ковры с коротким и длинным ворсом",
        "sections": [
            ("Какие ковры можно почистить", "Возможность работы зависит от состава, основы, устойчивости красителя и состояния изделия. Шерсть, вискоза, шёлк, клеевая основа и нестойкие цвета требуют особенно внимательной оценки."),
            ("Как подбираем способ", "Проверяем материал и краситель, локально обрабатываем загрязнения и используем подходящую технологию. Влажная экстракторная чистка подходит не каждому ковру — ограничения сообщаем до начала работы."),
            ("Что прислать для расчёта", "Нужны общий снимок, фото этикетки или состава при наличии, размеры и крупные планы пятен. Также сообщите о запахах и бытовых средствах, которыми уже пробовали чистить ковёр."),
            ("Стоимость и выезд", "Цена зависит от площади, длины ворса, состава и состояния. Условия чистки на месте и выезд по Витебской области согласуем отдельно."),
        ],
    },
    {
        "slug": "chistka-kovrolina",
        "short": "Ковролин",
        "card": "Чистка ковролина",
        "title": "Химчистка ковролина в Витебске",
        "description": "Выездная химчистка ковролина в квартирах, офисах и коммерческих помещениях Витебска. Расчёт по площади, материалу и степени загрязнения.",
        "lead": "Чистим ковролин в жилых и коммерческих помещениях. Площадь, материал, заставленность и состояние покрытия оцениваем до заказа.",
        "keywords": "ковролин в квартирах и офисах",
        "sections": [
            ("Где чистим ковролин", "Работаем в квартирах, домах, офисах и других помещениях, если покрытие и условия позволяют выполнить безопасную влажную обработку. Для оценки укажите примерную площадь и назначение помещения."),
            ("Подготовка помещения", "Уберите мелкие вещи и заранее сообщите, какую мебель возможно переместить. Если покрытие частично закрыто тяжёлыми предметами, согласуем доступную площадь до приезда."),
            ("Пятна и проходные зоны", "Особое внимание уделяем входным участкам, проходам и локальным загрязнениям. Полное восстановление изношенного или выцветшего ворса невозможно, потому что это уже изменение материала, а не грязь."),
            ("Высыхание после чистки", "Помещению требуется проветривание, а покрытию — время без активной нагрузки. Ориентир по высыханию зависит от основания, плотности ворса, температуры и воздухообмена."),
        ],
    },
    {
        "slug": "himchistka-avto",
        "short": "Салон автомобиля",
        "card": "Химчистка салона авто",
        "title": "Химчистка салона автомобиля в Витебске",
        "description": "Химчистка салона авто в Витебске: сиденья, тканевая обивка, ковролин и багажник. Реальные фото до и после, оценка по состоянию салона.",
        "lead": "Чистим сиденья, тканевую обивку, напольное покрытие и другие согласованные зоны салона. Состав работы определяем по фотографиям и осмотру.",
        "keywords": "сиденья, обивка, ковролин и багажник автомобиля",
        "sections": [
            ("Какие зоны можно очистить", "Можно заказать обработку сидений, тканевой обивки, напольного покрытия и багажника. Потолок, дверные карты, отдельные детали и локальная чистка рассчитываются после оценки."),
            ("Почему нужен предварительный осмотр", "В салоне сочетаются разные материалы, клеевые соединения, датчики и электрические элементы. Подбираем способ и допустимую влажность с учётом конструкции автомобиля."),
            ("Как подготовить автомобиль", "Уберите личные вещи из салона, дверных карманов и багажника, если он входит в заказ. Сообщите о запахах, старых пятнах и предыдущих попытках их удалить."),
            ("Высыхание и использование", "После влажной обработки материалы должны высохнуть. Срок зависит от объёма, погоды и вентиляции. Источник стойкого запаха иногда требует отдельной работы и не всегда устраняется одной чисткой."),
        ],
    },
    {
        "slug": "moika-okon",
        "short": "Окна и витрины",
        "card": "Мойка окон и витрин",
        "title": "Мойка окон и витрин в Витебске",
        "description": "Мойка окон, рам, подоконников, балконного остекления и витрин в Витебске. Согласование объёма и доступа, оценка стоимости по фото.",
        "lead": "Моем стекло и согласованные элементы окон: рамы, подоконники, откосы и сетки. Витрины и балконное остекление рассчитываем по площади и доступу.",
        "keywords": "окна, рамы, витрины и балконное остекление",
        "sections": [
            ("Что входит в мойку окон", "Отдельно согласуем стекло, рамы, подоконники, откосы и москитные сетки. Для витрин нужны примерные размеры, высота и информация о доступе с обеих сторон."),
            ("Балконы и большие витрины", "Количество створок не всегда отражает реальный объём. Панорамное или балконное остекление оцениваем по фото, площади и способу открывания."),
            ("Доступ и безопасность", "Перед записью обсуждаем этаж, открывание створок и возможность безопасно добраться до внешней поверхности. Высотные и недоступные зоны не включаются в обычную мойку автоматически."),
            ("Как подготовиться", "Освободите подоконники и проход к окнам, уберите хрупкие предметы. Если на стекле есть краска, клей, цемент или монтажная пена, обязательно покажите это на фото."),
        ],
    },
    {
        "slug": "moika-okon-posle-remonta",
        "short": "Окна после ремонта",
        "card": "Окна после ремонта",
        "title": "Мойка окон после ремонта в Витебске",
        "description": "Мойка окон после ремонта и строительства в Витебске: оценка следов краски, клея, цемента и плёнки, безопасный подбор инструмента и средств.",
        "lead": "Следы ремонта требуют отдельной оценки: краска, клей, цементная пыль и защитная плёнка удаляются по-разному. Сначала просим подробные фотографии стекла и рам.",
        "keywords": "окна со следами ремонта и строительства",
        "sections": [
            ("Чем отличается мойка после ремонта", "Обычная пыль и разводы смываются иначе, чем клей, краска, штукатурка или цемент. Неверный инструмент может поцарапать стекло или повредить профиль, поэтому вид загрязнения важно определить заранее."),
            ("Что показать на фотографиях", "Снимите окно полностью, отдельно рамы и крупным планом сложные следы. Укажите количество створок, этаж, способ открывания и есть ли доступ к внешней стороне."),
            ("Какие ограничения возможны", "Некоторые строительные составы химически повреждают профиль или стекло, а старая защитная плёнка разрушается от солнца. После осмотра объясним, что относится к загрязнению, а что уже стало повреждением поверхности."),
            ("Как рассчитывается стоимость", "Учитываем количество и площадь окон, набор элементов, сложность загрязнений и доступ. Итоговую цену и состав работ согласуем до начала мойки."),
        ],
    },
]

SERVICE_BY_SLUG = {service["slug"]: service for service in SERVICES}
FEATURED = [
    "himchistka-mebeli", "himchistka-divanov", "himchistka-matrasov",
    "himchistka-kresel-stulev", "himchistka-kovrov", "chistka-kovrolina",
    "himchistka-avto", "moika-okon",
]
PAIRS = [
    (3938, "Светлый угловой диван", "Мягкая мебель"),
    (3930, "Заднее сиденье автомобиля", "Салон авто"),
    (3934, "Бирюзовый диван", "Мягкая мебель"),
    (3944, "Матрас", "Матрасы"),
    (3946, "Автомобильное кресло", "Салон авто"),
    (3948, "Напольное покрытие салона", "Салон авто"),
    (3942, "Переднее сиденье автомобиля", "Салон авто"),
    (3928, "Диван с тканевой обивкой", "Мягкая мебель"),
]
FAQ = [
    ("Сколько стоит химчистка?", "Стоимость зависит от размера, материала и загрязнений. Пришлите в Viber общий снимок и фото пятен: обсудим объём и предварительную цену. Итоговую стоимость согласуем до начала работы."),
    ("Вы приезжаете на дом?", "Да, выезжаем по Витебску и Витебской области. Условия выезда за город, доступ к воде и электричеству уточняем при записи."),
    ("Можно ли убрать любое пятно?", "Не всегда. Результат зависит от происхождения и давности пятна, материала и предыдущих обработок. Выгорание, износ и повреждение красителя чистка не исправляет."),
    ("Сколько сохнет мебель?", "Время зависит от ткани, наполнителя, объёма влажной обработки, температуры и вентиляции. Ориентир мастер сообщит после оценки. Пользоваться мебелью стоит после полного высыхания."),
    ("Что подготовить до приезда?", "Освободите доступ к мебели или покрытию, уберите личные и хрупкие вещи. Для мойки окон освободите подоконники. Остальные детали уточним при записи."),
    ("Как отправить фотографии?", f"Откройте Viber по ссылке на сайте или позвоните по номеру {PHONE_DISPLAY}. В сообщении приложите общий вид, проблемные участки и коротко опишите задачу."),
]


def logo(prefix="./"):
    return f'<a class="logo" href="{prefix}" aria-label="Витклинер — главная"><span class="logo-mark">{icon("spark")}</span><span>витклинер<small>ХИМЧИСТКА И КЛИНИНГ</small></span></a>'


def button(text, href, kind="primary", extra=""):
    return f'<a class="btn btn-{kind}" href="{href}" {extra}>{text}{icon("arrow")}</a>'


def header(prefix):
    links = "".join(
        f'<a href="{prefix}#{anchor}">{text}</a>'
        for anchor, text in [("directions", "Услуги"), ("portfolio", "Работы"), ("process", "Как работаем"), ("prices", "Стоимость"), ("faq", "Вопросы")]
    )
    return f'''<a class="skip" href="#main">Перейти к содержанию</a><header class="header"><div class="wrap header-inner">{logo(prefix)}<nav class="nav" aria-label="Основное меню">{links}</nav><a class="header-phone" href="tel:{PHONE}"><span>{PHONE_DISPLAY}</span><small>Витебск и область</small></a><button class="menu-toggle" type="button" aria-label="Открыть меню" aria-expanded="false" aria-controls="mobile-nav">{icon('menu')}</button></div><nav class="mobile-nav" id="mobile-nav" aria-label="Мобильное меню" hidden>{links}<a href="{VIBER}" rel="noopener">Написать в Viber</a></nav></header>'''


def footer(prefix):
    service_links = "".join(f'<a href="{prefix}{SERVICE_BY_SLUG[slug]["slug"]}/">{SERVICE_BY_SLUG[slug]["card"]}</a>' for slug in FEATURED)
    return f'''<footer class="footer"><div class="wrap footer-grid"><div>{logo(prefix)}<p>Выездная химчистка и мойка окон<br>в Витебске и Витебской области.</p></div><nav class="footer-services" aria-label="Услуги"><strong>Услуги</strong>{service_links}</nav><div class="footer-contact"><strong>Связаться</strong><a href="tel:{PHONE}">{PHONE_DISPLAY}</a><a href="{VIBER}" rel="noopener">Написать в Viber</a><a href="{prefix}stoimost/">Как рассчитывается цена</a><a href="{prefix}privacy/">Конфиденциальность</a></div></div><div class="wrap footer-bottom"><span>© 2026 Витклинер</span><span>Витебск и область</span></div></footer><div class="mobile-bar" aria-label="Быстрая связь"><a class="btn btn-light" href="tel:{PHONE}">{icon('phone')}Позвонить</a><a class="btn btn-primary" href="{prefix}#contact">Оценка по фото{icon('arrow')}</a></div>'''


def faq(items=FAQ):
    return '<div class="faq-list">' + "".join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in items) + "</div>"


def contact(selected=""):
    options = "".join(f'<option{" selected" if s["short"] == selected else ""}>{E(s["short"])}</option>' for s in SERVICES) + '<option>Несколько услуг / другое</option>'
    return f'''<section id="contact" class="contact-section"><div class="wrap contact-grid"><div class="contact-copy"><span class="eyebrow">Оценка по фотографиям</span><h2>Покажите задачу.<br><em>Мы скажем по делу.</em></h2><p>Пришлите общий снимок и крупные фото загрязнений. Обсудим возможности чистки, стоимость и удобное время до выезда.</p><a class="contact-phone" href="tel:{PHONE}">{icon('phone')}{PHONE_DISPLAY}</a><p class="contact-subnote">Витебск и область · выезд по договорённости</p><div class="contact-direct">{button('Написать в Viber', VIBER, 'outline', 'rel="noopener"')}{button('Позвонить', f'tel:{PHONE}', 'outline')}</div></div><div class="contact-form"><span class="form-kicker">Быстрый запрос</span><h3>Подготовить сообщение</h3><p>Заполните три поля — сайт соберёт текст, который останется отправить в Viber вместе с фото.</p><form id="request-form"><label class="field" for="service">Что нужно почистить<select id="service" name="service">{options}</select></label><label class="field" for="location">Город или населённый пункт<input id="location" name="location" value="Витебск" required maxlength="100" autocomplete="address-level2"></label><label class="field" for="details">Коротко о задаче <span>(необязательно)</span><textarea id="details" name="details" maxlength="1000" placeholder="Например: угловой диван, пятна на сиденье"></textarea></label><button class="btn btn-primary" type="submit">Подготовить сообщение{icon('arrow')}</button><p class="form-note">Данные обрабатываются только в вашем браузере и не отправляются автоматически.</p></form><div class="request-result" id="request-result" hidden aria-live="polite"><h4>Сообщение готово</h4><div class="request-preview" id="request-preview"></div><button class="btn copy-btn" id="copy-request" type="button">Скопировать текст</button><a class="btn btn-primary" href="{VIBER}" rel="noopener">Открыть Viber{icon('arrow')}</a><p id="copy-status">Вставьте текст в чат и приложите фотографии.</p></div><noscript><p class="form-note">Включите JavaScript или сразу позвоните / напишите в Viber.</p></noscript></div></div></section>'''


def schema_graph(title, description, url, extra=None):
    catalog = {"@type": "OfferCatalog", "name": "Услуги Витклинер", "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["card"], "url": BASE + s["slug"] + "/"}} for s in SERVICES]}
    graph = [
        {"@type": "LocalBusiness", "@id": BASE + "#company", "name": "Витклинер", "alternateName": "VITCLEANER", "url": BASE, "telephone": PHONE, "logo": BASE + "assets/logo.svg", "image": BASE + "assets/og-cover.jpg", "priceRange": "₽₽", "areaServed": [{"@type": "City", "name": "Витебск"}, {"@type": "AdministrativeArea", "name": "Витебская область"}], "contactPoint": {"@type": "ContactPoint", "telephone": PHONE, "contactType": "customer service", "availableLanguage": "ru", "areaServed": "BY"}, "hasOfferCatalog": catalog},
        {"@type": "WebSite", "@id": BASE + "#website", "url": BASE, "name": "Витклинер", "inLanguage": "ru", "publisher": {"@id": BASE + "#company"}},
        {"@type": "WebPage", "@id": url + "#page", "url": url, "name": title, "description": description, "inLanguage": "ru", "isPartOf": {"@id": BASE + "#website"}, "about": {"@id": BASE + "#company"}, "dateModified": LASTMOD},
    ]
    if url != BASE:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Главная", "item": BASE}, {"@type": "ListItem", "position": 2, "name": title, "item": url}]})
    if extra:
        graph.extend(extra)
    return {"@context": "https://schema.org", "@graph": graph}


def document(title, description, body, path="", extra=None, noindex=False, home=False):
    prefix, url = ("./" if not path else "../"), BASE + path
    schema = json.dumps(schema_graph(title, description, url, extra), ensure_ascii=False).replace("</", "<\\/")
    preload = '<link rel="preload" as="image" href="assets/hero.webp" fetchpriority="high">' if home else ""
    robots = "noindex,follow" if noindex else "index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><meta name="description" content="{E(description)}"><meta name="robots" content="{robots}"><meta name="theme-color" content="#123d32"><meta name="color-scheme" content="light"><meta name="geo.region" content="BY-VI"><meta name="geo.placename" content="Витебск"><link rel="canonical" href="{url}"><meta property="og:type" content="website"><meta property="og:locale" content="ru_RU"><meta property="og:site_name" content="Витклинер"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(description)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}assets/og-cover.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Витклинер — химчистка и клининг в Витебске"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(description)}"><meta name="twitter:image" content="{BASE}assets/og-cover.jpg"><link rel="icon" href="{prefix}assets/logo.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="{prefix}assets/apple-touch-icon.png">{preload}<link rel="stylesheet" href="{prefix}assets/site.css?v=20261021c"><script src="{prefix}assets/site.js" defer></script><script type="application/ld+json">{schema}</script>{METRIKA_SCRIPT}</head><body>{METRIKA_NOSCRIPT}{header(prefix)}<main id="main">{body}</main>{footer(prefix)}</body></html>'''


def write(path, content):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def gallery():
    cards = ""
    for index, (number, title, category) in enumerate(PAIRS):
        images = ""
        for offset, status in enumerate(("До", "После")):
            path = ROOT / f"assets/work/img_{number + offset}.webp"
            width, height = Image.open(path).size
            images += f'<button class="work-image" type="button" data-zoom="assets/work/img_{number + offset}.webp" data-alt="{E(title)} — {status.lower()} чистки" aria-label="Увеличить фото: {E(title)}, {status.lower()} чистки"><img src="assets/work/img_{number + offset}.webp" alt="{E(title)} — {status.lower()} химчистки" width="{width}" height="{height}" loading="lazy" decoding="async"><span class="image-label{" after" if offset else ""}">{status}</span></button>'
        cards += f'<article class="work-card"><div class="work-images">{images}</div><div class="work-footer"><div><span class="work-index">0{index + 1}</span><h3>{E(title)}</h3></div><span class="work-tag">{E(category)}</span></div></article>'
    return f'''<section id="portfolio" class="section portfolio-section"><div class="wrap"><div class="section-head"><div><span class="eyebrow">Только реальные работы</span><h2>Не обещания.<br><em>Результат.</em></h2></div><p>Один объект до и после обработки. Без стоковых фотографий в портфолио и без цветокоррекции, которая приукрашивает результат.</p></div><div class="work-grid">{cards}</div><p class="gallery-footnote">Освещение и ракурс на фотографиях могут отличаться. Результат конкретной чистки зависит от материала, износа и происхождения загрязнений.</p></div></section><dialog class="image-dialog" id="image-dialog" aria-label="Увеличенная фотография"><button class="dialog-close" type="button" aria-label="Закрыть фотографию">×</button><img id="dialog-image" alt=""><p class="dialog-caption" id="dialog-caption"></p></dialog>'''


def service_directory():
    rows = ""
    for index, slug in enumerate(FEATURED):
        service = SERVICE_BY_SLUG[slug]
        rows += f'<a class="direction-row" href="{service["slug"]}/"><span class="direction-num">{index + 1:02d}</span><span><strong>{E(service["card"])}</strong><small>{E(service["keywords"])}</small></span>{icon("arrow")}</a>'
    return f'''<section id="directions" class="section directions-section"><div class="wrap"><div class="section-head"><div><span class="eyebrow">Все основные направления</span><h2>Выберите, что<br><em>нужно почистить.</em></h2></div><p>У каждой услуги — отдельная страница с процессом, ограничениями и подготовкой. Без случайных картинок и лишнего шума.</p></div><div class="directions-grid">{rows}</div><div class="directions-note"><span>{icon('spark')}</span><p><strong>Другая задача?</strong> Также обсуждаем кожаную мебель, окна после ремонта и комплекс из нескольких услуг.</p><a class="arrow-link" href="#contact">Спросить в Viber{icon('arrow')}</a></div></div></section>'''


def home_page():
    trust = "".join(f'<div class="trust-item">{icon(name)}<div><strong>{title}</strong><span>{subtitle}</span></div></div>' for name, title, subtitle in [("clock", "Более 10 лет опыта", "Знаем особенности материалов"), ("pin", "Выезд к вам", "Витебск и область"), ("wallet", "Цена до начала", "Согласуем объём заранее"), ("photo", "Реальные работы", "Фото до и после без стоков")])
    steps = "".join(f'<div class="step"><span class="step-num">0{i + 1}</span><div><h3>{title}</h3><p>{text}</p></div></div>' for i, (title, text) in enumerate([("Показываете задачу", "Присылаете общий вид, пятна и размеры в Viber."), ("Получаете понятную оценку", "Обсуждаем возможности, состав работы и стоимость."), ("Подбираем способ", "Проверяем материал и только затем начинаем чистку."), ("Принимаете результат", "Показываем работу и объясняем правила высыхания.")]))
    price_rows = "".join(f'<div class="price-row">{icon(name)}<div><strong>{title}</strong><p>{text}</p></div></div>' for name, title, text in [("fabric", "Размер и материал", "Тип обивки, площадь покрытия или количество створок."), ("spark", "Состояние", "Пятна, запахи, износ и предыдущие обработки."), ("pin", "Место и объём", "Адрес выезда, доступ и количество изделий.")])
    body = f'''<section class="hero"><img class="hero-img" src="assets/hero.webp" alt="Светлая гостиная с чистым тканевым диваном" width="1774" height="887" fetchpriority="high"><div class="hero-shade"></div><div class="wrap hero-layout"><div class="hero-content"><span class="location-pill">{icon('pin')}Витебск и Витебская область</span><h1>Чистая мебель.<br><em>Спокойный дом.</em></h1><p class="hero-lead">Выездная химчистка мебели, ковров и салона авто. Мойка окон. Оценка по фотографиям до приезда.</p><div class="hero-actions">{button('Оценить по фото', '#contact')}{button('Посмотреть работы', '#portfolio', 'light')}</div><p class="hero-note">{icon('check')}Объём и стоимость согласуем до начала работы</p></div><aside class="hero-card"><span>Витклинер</span><strong>Сначала смотрим.<br>Потом обещаем.</strong><p>Честно объясним, что можно очистить, а что относится к износу или повреждению материала.</p><a href="#process">Как проходит работа{icon('arrow')}</a></aside></div></section><div class="wrap"><div class="trust-strip">{trust}</div></div>{service_directory()}{gallery()}<section id="process" class="section section-white"><div class="wrap process-layout"><div class="process-photo"><img src="assets/process.webp" alt="Экстракторная чистка тканевой обивки" width="1024" height="1536" loading="lazy" decoding="async"><div class="photo-caption"><span>01</span><div><strong>Бережно к материалу</strong><p>Способ чистки выбираем после оценки поверхности.</p></div></div></div><div class="process-copy"><span class="eyebrow">Как мы работаем</span><h2>Понятно на каждом<br><em>этапе.</em></h2><p>Более 10 лет работаем с мебелью и покрытиями. Не начинаем с универсального средства: сначала оцениваем материал, состояние и ограничения.</p><div class="steps">{steps}</div></div></div></section><section id="prices" class="section price-section"><div class="wrap"><div class="price-panel"><div><span class="eyebrow">Цена без сюрпризов</span><h2>Расчёт под<br><em>вашу задачу.</em></h2><p>Пришлите фотографии и размеры. Назовём предварительную стоимость, а окончательный объём согласуем до начала работы.</p>{button('Получить оценку', '#contact')}<a class="price-more" href="stoimost/">Подробнее о расчёте{icon('arrow')}</a></div><div class="price-list">{price_rows}</div></div></div></section><section id="faq" class="section section-white"><div class="wrap faq-grid"><div class="faq-copy"><span class="eyebrow">Коротко о важном</span><h2>Вопросы<br><em>перед заказом.</em></h2><p>Если вашей ситуации нет в списке, пришлите фото — ответим предметно.</p></div>{faq()}</div></section>{contact()}'''
    extra = [{"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]
    write("index.html", document("Химчистка мебели в Витебске на дому — Витклинер", "Химчистка диванов, кресел, матрасов, ковров и салона авто в Витебске и области. Мойка окон, выезд, оценка по фото и реальные работы до и после.", body, extra=extra, home=True))


def related_links(current):
    related = [service for service in SERVICES if service["slug"] != current][:6]
    return "".join(f'<a href="../{s["slug"]}/">{E(s["card"])}{icon("arrow")}</a>' for s in related)


def service_pages():
    faq_schema = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ[:4]]}
    for service in SERVICES:
        sections = "".join(f'<section><h2>{E(title)}</h2><p>{E(text)}</p></section>' for title, text in service["sections"])
        body = f'''<div class="wrap"><nav class="breadcrumb" aria-label="Хлебные крошки"><a href="../">Главная</a><span>/</span><span>{E(service['short'])}</span></nav><section class="page-hero"><div><span class="eyebrow">Витклинер · Витебск и область</span><h1>{E(service['title'])}</h1><p>{E(service['lead'])}</p><div class="hero-actions">{button('Оценить по фото', '#contact')}{button('Смотреть работы', '../#portfolio', 'light')}</div></div><div class="page-proof"><span>{icon('check')}</span><strong>Стоимость заранее</strong><p>Пришлите фотографии и описание. До выезда обсудим состав работы и предварительную цену.</p></div></section></div><section class="section section-white"><div class="wrap article-grid"><article class="article-content">{sections}<section><h2>Заказать услугу в Витебске</h2><p>Позвоните по номеру <a class="text-link" href="tel:{PHONE}">{PHONE_DISPLAY}</a> или отправьте фотографии в Viber. Уточним объём, адрес, условия и удобное время. Выезд по Витебской области согласуем отдельно.</p></section></article><aside class="aside-box"><span class="eyebrow">Другие услуги</span><nav aria-label="Другие услуги">{related_links(service['slug'])}</nav><a class="btn btn-primary" href="#contact">Обсудить заказ{icon('arrow')}</a></aside></div></section><section class="section service-faq"><div class="wrap faq-grid"><div class="faq-copy"><span class="eyebrow">До приезда мастера</span><h2>Что важно<br><em>знать.</em></h2></div>{faq(FAQ[:4])}</div></section>{contact(service['short'])}'''
        service_schema = {"@type": "Service", "@id": BASE + service["slug"] + "/#service", "name": service["title"], "serviceType": service["short"], "description": service["description"], "provider": {"@id": BASE + "#company"}, "areaServed": [{"@type": "City", "name": "Витебск"}, {"@type": "AdministrativeArea", "name": "Витебская область"}], "url": BASE + service["slug"] + "/"}
        write(service["slug"] + "/index.html", document(service["title"] + " — Витклинер", service["description"], body, service["slug"] + "/", extra=[service_schema, faq_schema]))


def utility_pages():
    rows = "".join(f'<li><a class="text-link" href="../{s["slug"]}/">{E(s["card"])}</a> — {E(s["keywords"])}.</li>' for s in SERVICES)
    price_body = f'''<div class="wrap"><nav class="breadcrumb" aria-label="Хлебные крошки"><a href="../">Главная</a><span>/</span><span>Стоимость</span></nav><section class="page-hero"><div><span class="eyebrow">Расчёт до начала работ</span><h1>Стоимость химчистки и клининга в Витебске</h1><p>Рассчитаем задачу по фото и описанию. Согласуем стоимость и состав заказа до начала работы.</p><div class="hero-actions">{button('Получить оценку', '#contact')}</div></div><div class="page-proof"><span>{icon('wallet')}</span><strong>Без случайной цены</strong><p>Учитываем реальный размер, материал, состояние и условия работы.</p></div></section></div><section class="section section-white"><article class="wrap plain-content"><h2>Почему цена рассчитывается индивидуально</h2><p>Небольшое кресло, угловой диван, матрас и автомобильный салон требуют разного времени и расхода средств. Учитываем материал, размер, загрязнения, условия доступа и адрес выезда.</p><h2>Что прислать для оценки</h2><ul><li>Общий снимок изделия или поверхности.</li><li>Крупные фото пятен и проблемных участков.</li><li>Размеры, количество изделий, окон или сидений.</li><li>Город или населённый пункт.</li><li>Информацию о материале и предыдущей чистке, если она известна.</li></ul><h2>По каким услугам можно получить расчёт</h2><ul class="service-list">{rows}</ul><h2>Как согласуем заказ</h2><p>По фото обсуждаем предполагаемый объём и стоимость. Если при осмотре обнаружатся дополнительные задачи, сначала согласуем их с вами. Выезд по области и особые условия обсуждаем до записи.</p></article></section>{contact()}'''
    write("stoimost/index.html", document("Стоимость химчистки мебели и клининга в Витебске — Витклинер", "От чего зависит цена химчистки дивана, матраса, ковра, салона авто и мойки окон в Витебске. Оценка по фото до начала работ.", price_body, "stoimost/"))
    privacy_body = f'''<div class="wrap"><nav class="breadcrumb" aria-label="Хлебные крошки"><a href="../">Главная</a><span>/</span><span>Конфиденциальность</span></nav><article class="plain-content privacy-content"><h1>Конфиденциальность</h1><p>Эта страница объясняет, как работает подготовка сообщения на сайте Витклинер.</p><h2>Форма на сайте</h2><p>Поля обрабатываются в вашем браузере. Сайт не отправляет введённый текст на сервер и не сохраняет его. Сообщение попадает в Viber только после того, как вы сами откроете чат и нажмёте отправку.</p><h2>Телефон и Viber</h2><p>Ссылки открывают приложение звонков или сторонний сервис Viber. У сторонних сервисов действуют собственные правила обработки данных. Передавайте только сведения, необходимые для оценки услуги.</p><h2>Хостинг и аналитика</h2><p>Хостинг может обрабатывать стандартные технические сведения о запросах. В текущей версии сайта нет рекламных пикселей, счётчиков аналитики и собственных cookies.</p><h2>Связь</h2><p>По вопросам обращения позвоните по номеру <a class="text-link" href="tel:{PHONE}">{PHONE_DISPLAY}</a>.</p></article></div>'''
    write("privacy/index.html", document("Конфиденциальность — Витклинер", "Как сайт Витклинер обрабатывает данные формы, подготавливает сообщение и открывает связь с компанией по телефону и через Viber.", privacy_body, "privacy/", noindex=True))
    not_found = f'''<div class="wrap"><section class="error-page"><span class="eyebrow">Ошибка 404</span><h1>Такой страницы нет</h1><p>Вернитесь на главную, выберите услугу или сразу свяжитесь с нами.</p><div class="hero-actions">{button('На главную', BASE)}{button('Позвонить', f'tel:{PHONE}', 'light')}</div></section></div>'''
    error = document("Страница не найдена — Витклинер", "Страница не найдена. Перейдите на главную Витклинер.", not_found, "404.html", noindex=True)
    base_path = urlsplit(BASE).path
    write("404.html", error.replace('href="../', f'href="{base_path}').replace('src="../', f'src="{base_path}'))


def technical_files():
    paths = [""] + [service["slug"] + "/" for service in SERVICES] + ["stoimost/"]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for path in paths:
        priority = "1.0" if not path else ("0.7" if path == "stoimost/" else "0.8")
        sitemap += f'  <url><loc>{X(BASE + path)}</loc><lastmod>{LASTMOD}</lastmod><changefreq>monthly</changefreq><priority>{priority}</priority></url>\n'
    write("sitemap.xml", sitemap + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\nHost: {urlsplit(BASE).netloc}\n")
    write(".nojekyll", "")


home_page()
service_pages()
utility_pages()
technical_files()
print(f"Generated home, {len(SERVICES)} service pages, pricing, privacy, 404 and sitemap for {BASE}")
