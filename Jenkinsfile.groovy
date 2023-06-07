pipeline {
    node{
        stages{
            stage("Build"){
                sh "python3 run.py --container cytopia/dvwa:latest"
            }
        }
    }
}