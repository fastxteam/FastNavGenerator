@echo off
chcp 65001 > nul
echo Generating navigation website...

python FastNavGenerator.py --config=FastNavGenerator.ini --output=index.html

if %errorlevel%==0 (
    echo Success: Navigation website generated successfully!
    echo File: index.html
) else (
    echo Error: Generation failed!
    pause
)