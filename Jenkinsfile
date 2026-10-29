pipeline {
    agent any
    environment {
        IMAGE = "priyaranjans27/payment-system:v3"
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Docker Build') {
            steps { bat 'docker build -t %IMAGE% .' }
        }
        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
                    bat 'docker login -u %DH_USER% -p %DH_PASS%'
                    bat 'docker push %IMAGE%'
                }
            }
        }
    }
}