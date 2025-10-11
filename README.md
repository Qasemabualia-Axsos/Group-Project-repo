# 🎥 RateUp — Movie Rating & Review Platform

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg?style=flat&logo=python)](https://www.python.org/) 
[![Django](https://img.shields.io/badge/Django-5.2-green.svg?style=flat&logo=django)](https://www.djangoproject.com/) 
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg?style=flat&logo=bootstrap)](https://getbootstrap.com/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)  
[![Issues](https://img.shields.io/github/issues/Jacob11Q1/Group-Project-repo.svg)](https://github.com/Jacob11Q1/Group-Project-repo/issues)

---

## 📖 About

**RateUp** is a collaborative Django-based web application for rating and reviewing movies, actors, and directors.  
It provides both **web views** and **API endpoints**, with responsive Bootstrap templates, media uploads, and seed data for testing.

The project is built as part of a group bootcamp to simulate a **real-world SaaS/IMDb-style application**.

---

## ✨ Features

- 🔑 **User Accounts** – Register, login, profile management  
- 🎬 **Movies** – Browse, add, edit, delete movies with covers  
- 🎭 **Actors & Directors** – Profiles, filmography, CRUD operations  
- 🏷️ **Categories** – Organize movies by genres/categories  
- ⭐ **Reviews & Ratings** – Users can post reviews and star ratings  
- 📡 **API Endpoints** – REST-like structure for external clients  
- 🖼️ **Media Uploads** – Actor photos, movie covers, profile images  
- 🌱 **Dummy Data Seeder** – Generate fake movies/actors for testing  
- 🎨 **Responsive UI** – Bootstrap 5 styling with hover effects  

---

## 🛠️ Tech Stack

| Layer        | Technology |
|--------------|------------|
| Backend      | Django 5.2 (Python 3.10+) |
| Database     | SQLite (default) / MySQL (optional) |
| Frontend     | Django Templates + Bootstrap 5.3 |
| Media/Static | Django static & media handling |
| APIs         | Django views / REST endpoints |

---

## 📂 Project Structure
├── accounts/ # User auth & profiles
├── actors/ # Actor model, views, templates
├── directors/ # Director model, views, templates
├── categories/ # Movie categories
├── movies/ # Movies + management command for dummy data
│ └── management/commands/populate_all_dummy.py
├── reviews/ # Reviews & rating logic
├── api/ # API endpoints
├── Group_project/ # Core settings & URLs
├── templates/ # Shared templates (base.html, index.html, etc.)
├── static/ # CSS, JS, images
├── media/ # Uploaded covers & actor photos
├── manage.py
└── README.md

---

## 🚀 Getting Started

### 1️⃣ Clone the Repo
```bash
git clone https://github.com/Jacob11Q1/Group-Project-repo.git
cd Group-Project-repo

2️⃣ Setup Environment
python -m venv venv
# Activate venv
venv\Scripts\activate   # Windows
source venv/bin/activate   # macOS/Linux

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run Migrations
python manage.py makemigrations
python manage.py migrate

5️⃣ Seed Dummy Data (optional)
python manage.py populate_all_dummy

6️⃣ Start Development Server
python manage.py runserver

Open http://localhost:8000
 🎉



📡 API Endpoints (Examples):
    Method	Endpoint	Description
    GET	/api/movies/	List all movies
    GET	/api/movies/<id>/	Get movie details
    POST	/api/movies/	Create new movie
    PUT	/api/movies/<id>/	Update movie
    DELETE	/api/movies/<id>/	Delete movie
    GET	/api/actors/	List all actors
    GET	/api/directors/	List all directors
    🌱 Dummy Data


The project ships with a management command to generate fake data:
python manage.py populate_all_dummy
This will create actors, directors, categories, movies, and reviews with sample images and bios.
🤝 Contributing


Contributions are welcome! 🚀
Fork the repo
Create a new branch: git checkout -b feature/your-feature
Commit changes: git commit -m "Add new feature"
Push branch: git push origin feature/your-feature
Open a Pull Request
Please follow PEP8 guidelines and update docs if needed.


📜 License:
    This project is licensed under the MIT License.
    See LICENSE
    for details.


🙏 Acknowledgments:
    Django & Python community
    AXSOS Academy Group Project Team
    Open source contributors & libraries
💡  “Movies inspire us, connect us, and tell the stories that matter.”