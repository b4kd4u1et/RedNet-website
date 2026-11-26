# rednet.kz — статический сайт команды RedNet

Одностраничный информационный сайт на чистых HTML + CSS: без JS, фреймворков, CDN, внешних шрифтов и трекеров.
Три языка — отдельные статические страницы: казахский `/` (основной), английский `/en/`, русский `/ru/`.
Блог (blog.rednet.kz, WordPress) — отдельный сайт, здесь только ссылка на него.

## Дерево файлов

```
static-site/
├── README.md                     — этот файл
├── nginx/
│   ├── rednet.kz.conf            — пример server-блоков nginx
│   └── security-headers.conf     — CSP, HSTS, X-Content-Type-Options, Referrer-Policy, Permissions-Policy и др.
└── public/                       — корень сайта (копируется на сервер целиком)
    ├── index.html                — казахская версия (/)
    ├── en/index.html             — английская версия (/en/)
    ├── ru/index.html             — русская версия (/ru/)
    ├── 404.html
    ├── assets/
    │   ├── style.css             — все стили
    │   ├── logo.svg              — логотип, прозрачный фон (исходный файл, без изменений)
    │   └── logo-square.svg       — логотип на фоне 1500×1500 (исходный файл, для соцсетей/аватарок)
    ├── favicon.svg               — буква «R» из логотипа на фоне логотипа
    ├── favicon-32.png
    ├── apple-touch-icon.png      — 180×180
    ├── og-image.png              — 1200×630, превью для соцсетей (Open Graph)
    ├── robots.txt
    └── sitemap.xml               — с hreflang-альтернативами
```

## Редактирование

* Тексты — черновики, каждый блок помечен `<!-- TODO: проверить текст -->`. Найти всё, что осталось доделать:
  `grep -rn TODO public/`
* Кредо: вставить финальный текст ru/en из README команды, kk — перевод (блок `.credo` в каждой странице).
* Telegram оставлен с пометкой TODO, Instagram не добавлен (нет ссылки) — место отмечено комментарием.
* Таблица соревнований одинаковая во всех трёх файлах — при правке меняйте все три.
* Цвета и контраст описаны в начале `assets/style.css`. Красный `#F53131` — только для крупного текста
  (≥ 24 px или ≥ 18,7 px жирным) и линий; мелкий текст — `--text` / `--muted`.

## Локальный просмотр

Пути абсолютные (`/assets/...`), поэтому открывайте через локальный сервер, а не как файл:

```bash
cd static-site/public && python3 -m http.server 8000
```

## Деплой на nginx

1. Скопировать файлы сайта на сервер:

```bash
rsync -av --delete static-site/public/ user@server:/var/www/rednet.kz/
```

2. На сервере выставить права (nginx должен читать файлы):

```bash
sudo chown -R root:root /var/www/rednet.kz && sudo find /var/www/rednet.kz -type d -exec chmod 755 {} + && sudo find /var/www/rednet.kz -type f -exec chmod 644 {} +
```

3. Положить конфиги:

```bash
sudo cp static-site/nginx/security-headers.conf /etc/nginx/snippets/rednet-security-headers.conf
```

```bash
sudo cp static-site/nginx/rednet.kz.conf /etc/nginx/sites-available/rednet.kz && sudo ln -s /etc/nginx/sites-available/rednet.kz /etc/nginx/sites-enabled/
```

4. Сертификат (если ещё нет). Сначала можно временно закомментировать два 443-блока, перезагрузить nginx, затем:

```bash
sudo mkdir -p /var/www/letsencrypt && sudo certbot certonly --webroot -w /var/www/letsencrypt -d rednet.kz -d www.rednet.kz
```

5. Проверить и применить:

```bash
sudo nginx -t && sudo systemctl reload nginx
```

6. Проверка заголовков:

```bash
curl -sI https://rednet.kz/ | grep -iE 'content-security|strict-transport|x-content-type|referrer|permissions'
```

### Заметки по заголовкам

* **CSP** строгий: `default-src 'none'`, разрешены только свои стили и картинки. Если когда-нибудь появятся
  JS, внешние картинки или inline-стили — CSP нужно расширить, иначе браузер их заблокирует.
* **HSTS** с `includeSubDomains`: включайте, только если HTTPS есть на всех поддоменах (в т.ч. blog.rednet.kz).
  Начать можно с `max-age=300`, убедиться, что всё работает, и поднять до года.
* В nginx `add_header` внутри `location` отменяет заголовки уровня `server`, поэтому сниппет подключается
  повторно в каждом `location` со своим `add_header`.

## Размер

HTML каждой страницы ~9 КБ, CSS ~8 КБ; без логотипа и PNG-превью страница весит < 20 КБ (лимит — 150 КБ).
