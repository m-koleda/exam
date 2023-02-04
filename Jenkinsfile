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
                        sh 'echo use docker-compose'
			sh 'docker-compose up -d'
                    }
                    elif (readFile('config.yaml').contains("use: 'ubuntu'")) {
                        sh 'echo use VM with Ubuntu'
			sh 'vagrant up --provision'
                    }
		    elif (readFile('config.yaml').contains("use: 'centos'")) {
                        sh 'echo use VM with Centos'
			sh 'vagrant up --provision'
                    }
		    else {
                        sh 'echo check config.yaml - use only docker or ubuntu or centos'
                    }
                }
                sh 'echo DEPLOY STAGE OK'
            }
        }
    }
}
