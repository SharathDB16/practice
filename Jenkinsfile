def img
pipeline {
    environment {
        registry = "sharathdb/python-project" //To push an image to Docker Hub, you must first name your local image using your Docker Hub username and the repository name that you created through Docker Hub on the web.
        registryCredential = 'DOCKERHUB'
        githubCredential = 'GITHUB'
        dockerImage = ''
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
        
        stage('Setup') {
            steps {
                script {
                    // Install Python 3 and pip
                    sh 'sudo apt-get update'
                    sh 'sudo apt-get install -y python3 python3-venv python3-pip'

                    // Create and activate a virtual environment
                    sh 'python3 -m venv venv'
                    sh '. venv/bin/activate'
                    
                    // Install dependencies
                    sh 'pip install --no-warn-script-location -r requirements.txt'  // If you have a requirements.txt file
                }
            }
        }

        stage ('Test'){
                steps {
                sh "pytest testRoutes.py"
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
                    
        stage('Deploy') {
           steps {
                sh label: '', script: "docker run -d --name ${JOB_NAME} -p 5000:5000 ${img}"
          }
        }

      }
    }