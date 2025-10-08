# SocialMediaAPI

**SocialMediaAPI** is a full-featured backend for a social media platform built with Django, GraphQL (Graphene), and JWT authentication. It supports user registration, login, post creation, sharing to followers or personal feed, and secure logout with token blacklisting.

---

## Features

- JWT Authentication (Access & Refresh Tokens)
- User Registration & Login
- Post Creation & Listing
- Share Posts to Followers or Feed
- User Feed Aggregation
- Secure Logout with Token Blacklisting
- GraphQL API with Graphene
- Django ORM for Models & Queries

---

## Tech Stack

- **Backend**: Django 4.x
- **API Layer**: Graphene-Django (GraphQL)
- **Auth**: Simple JWT + Graphene Custom Mutations
- **Database**: PostgreSQL (or SQLite for dev)
- **Static Files**: WhiteNoise Middleware
- **Token Blacklisting**: `rest_framework_simplejwt.token_blacklist`

---

## Installation

```bash
git clone https://github.com/yourusername/socialmediapi.git
cd socialmediapi
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
