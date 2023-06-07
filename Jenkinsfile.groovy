pipeline{
    agent none
        stages{
            stage("Build"){
                steps{
                sh "python3 run.py --container cytopia/dvwa:latest"
                }
            }
        }
    
}