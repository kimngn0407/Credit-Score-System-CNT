@echo off
echo Starting Spring Boot Backend...
echo.

REM Set environment variables for local development
set SPRING_DATASOURCE_URL=jdbc:postgresql://localhost:5432/LoanSystem
set SPRING_DATASOURCE_USERNAME=postgres
set SPRING_DATASOURCE_PASSWORD=Ngan0407@!
set CREDIT_SCORING_API_URL=http://localhost:8001
set CREDIT_NLG_API_URL=http://localhost:8002
set CREDIT_NLG_API_KEY=your-secret-key

echo Database URL: %SPRING_DATASOURCE_URL%
echo Credit Scoring API: %CREDIT_SCORING_API_URL%
echo.

REM Navigate to LoanSystem directory and run Spring Boot
cd /d "%~dp0\LoanSystem"
mvnw spring-boot:run

pause
