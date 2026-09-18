@echo off
title Dublaj Partisi - Baslatiliyor...
echo ====================================================
echo        DUBLAJ PARTISI (P2P WebRTC Oyunu)
echo ====================================================
echo.
echo Yerel test sunucusu baslatiliyor...
echo Tarayiciniz acilacak: http://localhost:3000
echo.
start http://localhost:3000
python server.py
pause
