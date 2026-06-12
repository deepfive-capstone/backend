@echo off
title Backend Server
call backend\.venv\Scripts\activate
uvicorn app.main:app
pause