<h1 align="center">Favorite Pro</h1>

<p align="center">
  <strong>Your personal ideas archive. Turn chaos from your saved messages into an organized collection.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-green.svg?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-blue.svg?logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Telegram-2CA5E0.svg?logo=telegram&logoColor=white" alt="Telegram Bot">
  <img src="https://img.shields.io/badge/Vue.js-4FC08D.svg?logo=vue.js&logoColor=white" alt="Vue.js">
  <img src="https://img.shields.io/badge/Docker-2496ED.svg?logo=docker&logoColor=white" alt="Docker">
</p>

## 🎯 The Problem

Every day, we save dozens of links, posts, videos, and memes to our "Saved Messages" in Telegram or other social media. Over time, this feed turns into chaos where it's impossible to find anything, and 80% of the saved content is forgotten forever. Valuable ideas and time are lost.

## 💡 The Solution: Izbranoe Pro

**"Izbranoe Pro"** is a tool that organizes your content into visual "boards" (similar to Pinterest). It transforms random saves into a structured "personal archive of ideas" with search and convenient access from any device.

## ✨ Tech Stack

| Component      | Technologies                             | Description                                                              |
|----------------|------------------------------------------|--------------------------------------------------------------------------|
| **Backend**    | `FastAPI`, `SQLAlchemy`, `PostgreSQL`    | A REST API to manage all data (users, boards, items).                    |
| **Telegram Bot** | `aiogram 3.x`                            | The primary client for quickly saving content.                           |
| **Web UI**     | `HTML`, `CSS`, `Vue.js`                  | A visual client for browsing boards and saved items in a web browser.    |
| **Environment**| `Docker`                                 | Containerization of the PostgreSQL database for easy deployment.         |

## 🚀 Key Features

*   **Quick Save via Telegram:** Simply send the bot any text, link, photo, video, voice message, or location.
*   **Title Prompt on Save:** The bot asks for a custom title for each item, so you'll never forget its context.
*   **Board Organization:** Create thematic boards (e.g., "To Read," "Vacation Ideas," "Recipes").
*   **Auto-Board Creation:** If you don't have any boards, the bot automatically creates the first one with the current date.
*   **Interactive Browsing:** Use bot commands or the web UI to browse the contents of your boards and open saved items.
*   **Full-Text Search:** Instantly find any item by its title using the `/search` command.
*   **Dual Clients:** Manage your archive through both a convenient Telegram bot and a clear, visual web interface.

---

## 🛠️ How to Run the Project Locally

**Prerequisites:** **Git**, **Python 3.10+**, **Docker Desktop**.

#### Step 1: Clone the Repository
```bash
# Replace the URL with your repository's address
git clone https://github.com/YourUsername/YourRepoName.git
cd YourRepoName
