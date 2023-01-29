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
        stage('Deploy'){
            steps {
                sh 'echo DEPLOYING...'
                sh 'vagrant up --provision'
                sh 'echo DEPLOY STAGE OK'
            }
        }
    }
}
