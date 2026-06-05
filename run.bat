@echo off
title Backend Server
call .venv\Scripts\activate
uvicorn app.main:app --reload
pause