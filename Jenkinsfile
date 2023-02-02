pipeline {
    agent {
        node 'built-in'
    }
    stages {
        stage('Build'){
            steps {
                sh 'echo BUILDING...'
                sh 'echo BUILD ID - ${BUILD_ID}'
                sh 'echo BUILD STAGE OK'
            }
        }
        stage('Test'){
            steps {
                sh 'echo TESTING...'
		sh 'python3 test.py'
            }
        }
        stage("Publish") {
            steps {
                sh 'echo DEPLOYING...'
                script {
                    if (readFile('config.yaml').contains("use: 'docker'")) {
                        sh 'docker-compose up -d'
                    }
                    else {
                        sh 'vagrant up --provision'
                    }
                }
                sh 'echo DEPLOY STAGE OK'
            }
        }
    }
}
