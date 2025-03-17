# Messaging App with Jenkins Pipeline

This project demonstrates a Python application with automated testing using Jenkins Pipeline.

## Project Structure
```
messaging_app/
├── Jenkinsfile
├── README.md
├── requirements.txt
└── messaging_app/
    ├── __init__.py
    └── tests/
        ├── __init__.py
        └── test_app.py
```

## Setup Instructions

### 1. Start Jenkins Container
```bash
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

### 2. Get Jenkins Initial Admin Password
```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### 3. Configure Jenkins
1. Access Jenkins at http://localhost:8080
2. Install required plugins:
   - Git plugin
   - Pipeline plugin
   - ShiningPanda Plugin
   - HTML Publisher plugin

### 4. Add GitHub Credentials
1. Go to "Manage Jenkins" → "Manage Credentials"
2. Add your GitHub credentials with ID: 'github-credentials'

### 5. Create Pipeline Job
1. Create new Pipeline job
2. Configure Git repository
3. Set Script Path to: messaging_app/Jenkinsfile

### 6. Run Pipeline
- Click "Build Now" to run the pipeline manually

## Testing
To run tests locally:
```bash
pip install -r requirements.txt
python -m pytest
``` 