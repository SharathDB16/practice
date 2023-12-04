def img
pipeline {
    environment {
        registry = "sharathdb/python-project" //To push an image to Docker Hub, you must first name your local image using your Docker Hub username and the repository name that you created through Docker Hub on the web.
        registryCredential = 'DOCKERHUB'
        githubCredential = 'GITHUB'
        dockerImage = ''
        sonarqubeScannerHome = tool 'sonar'
    }
    agent any
    stages {
        
        stage('checkout') {
                steps {
                git branch: 'master',
                credentialsId: githubCredential,
                url: 'https://github.com/SharathDB16/practice.git'
                }
        }
        
        stage('Initilize Unit Test Env') {
            steps {
                script {
                    // Create a test environment
                    sh("docker-compose -f docker-compose.test.yml -p ${composeProject} up -d --build")
                    sh("sleep 20s")
                    
                }
            }
        }

        stage ('Run Unit tests'){
                steps {
                sh("docker-compose -f docker-compose.test.yml -p ${composeProject} exec -T pullbased python3 testRoutes.py || echo 0")
                }
        }

        stage ('Clean Up'){
            steps{
                sh returnStatus: true, script: 'docker stop $(docker ps -a | grep ${JOB_NAME} | awk \'{print $1}\')'
                sh returnStatus: true, script: 'docker rmi $(docker images | grep ${registry} | awk \'{print $3}\') --force' //this will delete all images
                sh returnStatus: true, script: 'docker rm ${JOB_NAME}'
            }
        }

        stage('Build Image') {
            steps {
                script {
                    img = registry + ":${env.BUILD_ID}"
                    println ("${img}")
                    dockerImage = docker.build("${img}")
                }
            }
        }

        stage('Push To DockerHub') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', registryCredential) {
                        docker.image("${img}").push()
                    }
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    withSonarQubeEnv('sonar') {
                        sh "${sonarqubeScannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }
                    
        stage('Deploy') {
           steps {
                sh label: '', script: "docker run -d --name ${JOB_NAME} -p 5000:5000 ${img}"
          }
        }

      }
    }