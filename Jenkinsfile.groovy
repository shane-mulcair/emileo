pipeline{
    agent any
        stages{
            stage("Setup"){
                steps{
                    sh "sudo apt-get update && sudo apt-get install -y python3-pip"
                    sh "pip3 install --user docker"
                }
            }
            stage("Build"){
                steps{
                sh "python3 run.py --container cytopia/dvwa:latest"
                }
            }
        }
    
}