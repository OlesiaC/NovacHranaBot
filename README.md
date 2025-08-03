# Telegram Budget Bot

Телеграм-бот для контроля бюджета в группе.

---

## ✅ Функционал:
- Задание общего бюджета (`/set_budget`)
- Учёт трат участников (отправка числа)
- Рейтинг по тратам (`/top`)
- Сброс бюджета (`/reset_budget`)
- Запуск через Docker + docker-compose

---

## 🚀 Запуск проекта

### 1. Клонирование репозитория:
```bash
git clone https://github.com/OlesiaC/NovacHranaBot.git
cd NovacHranaBot
```
### 2. Создание файла `.env`:
```
BOT_TOKEN=токен_от_BotFather
```
### 3. Запуск через Docker:
```bash
docker compose up -d --build
```
