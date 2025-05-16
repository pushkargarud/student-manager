pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/pushkargarud/student-manager.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                script {
                    // Install dependencies (if any)
                    sh 'pip install -r requirements.txt'
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    // Run tests (if you have them)
                    sh 'pytest tests/'
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    // Add your deployment steps here
                    echo 'Deploying application...'
                }
            }
        }
    }
}
