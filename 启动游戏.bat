@echo off
chcp 65001 >nul
setlocal
set "GAME_DIR=%~dp0."
set "RENPY_SDK=D:\renpy\renpy-8.5.3-sdk"

if not exist "%RENPY_SDK%\renpy.py" (
    echo.
    echo 未找到 Ren'Py SDK：%RENPY_SDK%
    echo.
    echo 请先安装 Ren'Py 8.5.3，或修改本文件里的 RENPY_SDK 路径。
    echo 也可以用 Ren'Py Launcher 手动选择本项目目录启动。
    echo.
    pause
    exit /b 1
)

set "RENPY_PATH_TO_SAVES=%GAME_DIR%\saves"
start "" "%RENPY_SDK%\lib\py3-windows-x86_64\python.exe" "%RENPY_SDK%\renpy.py" "%GAME_DIR%" run
