@echo off
echo ======================================================================
echo  CRIMEATHON '26 — OPENING OFFICIAL REPORT & PRESENTATION SLIDES
echo ======================================================================
echo.
echo Opening Executive DFIR Investigation Report (Print / PDF ready)...
start "" "%~dp0reports\EXECUTIVE_REPORT.html"

echo.
echo Opening 16:9 Presentation Slides Deck (Interactive Slide Viewer)...
start "" "%~dp0reports\PRESENTATION_SLIDES.html"

echo.
echo ======================================================================
echo Done! Both have opened in your default browser.
echo Press any key to exit.
pause >nul
