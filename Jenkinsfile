pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'docker build -t my_project .'
            }
        }
        stage('Test') {
            steps {
                sh 'docker run my_project pytest'
            }
        }
        stage('Deploy') {
            steps {
                // Add deployment steps here
            }
        }
    }
}
