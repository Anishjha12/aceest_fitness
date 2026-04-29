// ──────────────────────────────────────────────────────────────
// ACEest Fitness & Gym – Jenkins CI/CD Pipeline
// ──────────────────────────────────────────────────────────────
pipeline {
    agent any

    environment {
        APP_NAME        = "aceest-fitness"
        DOCKER_REGISTRY = "docker.io"
        DOCKER_IMAGE    = "${DOCKER_REGISTRY}/<anishjha12>/${APP_NAME}"
        IMAGE_TAG       = "${BUILD_NUMBER}"
        SONAR_PROJECT   = "aceest-fitness"
        KUBECONFIG_CRED = "kubeconfig-credentials"
        GITHUB_REPO     = "https://github.com/Anishjha12/aceest_fitness"
    }

    triggers {
        // Poll GitHub every minute for new commits
        pollSCM("* * * * *")
    }

    stages {

        // ── 1. Checkout ────────────────────────────────────────
        stage("Checkout") {
            steps {
                git branch: "main", url: "${GITHUB_REPO}"
                echo "Code checked out from GitHub"
            }
        }

        // ── 2. Setup Python Environment ────────────────────────
        stage("Setup Environment") {
            steps {
                sh """
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }

        // ── 3. Unit Tests + Coverage ───────────────────────────
        stage("Unit Tests") {
            steps {
                sh """
                    . venv/bin/activate
                    pytest tests/ \\
                        --cov=app \\
                        --cov-report=xml:coverage.xml \\
                        --cov-report=html:htmlcov \\
                        --junitxml=test-results.xml \\
                        -v
                """
            }
            post {
                always {
                    junit "test-results.xml"
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: "htmlcov",
                        reportFiles: "index.html",
                        reportName: "Coverage Report"
                    ])
                }
            }
        }

        // ── 4. SonarQube Analysis ──────────────────────────────
        stage("SonarQube Analysis") {
            environment {
                SONAR_TOKEN = credentials("sonar-token")
            }
            steps {
                withSonarQubeEnv("SonarQube") {
                    sh """
                        sonar-scanner \\
                            -Dsonar.projectKey=${SONAR_PROJECT} \\
                            -Dsonar.projectName="ACEest Fitness" \\
                            -Dsonar.sources=app \\
                            -Dsonar.tests=tests \\
                            -Dsonar.python.coverage.reportPaths=coverage.xml \\
                            -Dsonar.python.version=3.11
                    """
                }
            }
        }

        // ── 5. SonarQube Quality Gate ──────────────────────────
        stage("Quality Gate") {
            steps {
                timeout(time: 5, unit: "MINUTES") {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        // ── 6. Build Docker Image ──────────────────────────────
        stage("Build Docker Image") {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:${IMAGE_TAG}")
                    docker.build("${DOCKER_IMAGE}:latest")
                }
                echo "Docker image built: ${DOCKER_IMAGE}:${IMAGE_TAG}"
            }
        }

        // ── 7. Push to Docker Hub ──────────────────────────────
        stage("Push Docker Image") {
            steps {
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", "dockerhub-credentials") {
                        dockerImage.push("${IMAGE_TAG}")
                        dockerImage.push("latest")
                    }
                }
                echo "Image pushed to Docker Hub"
            }
        }

        // ── 8. Deploy to Kubernetes (Rolling Update) ───────────
        stage("Deploy – Rolling Update") {
            steps {
                withKubeConfig([credentialsId: "${KUBECONFIG_CRED}"]) {
                    sh """
                        kubectl set image deployment/aceest-fitness \\
                            aceest-fitness=${DOCKER_IMAGE}:${IMAGE_TAG} \\
                            --namespace=aceest
                        kubectl rollout status deployment/aceest-fitness --namespace=aceest
                    """
                }
            }
        }

        // ── 9. Smoke Test after Deployment ────────────────────
        stage("Smoke Test") {
            steps {
                sh """
                    sleep 10
                    curl -f http://<CLUSTER_ENDPOINT>/  || exit 1
                    echo "Smoke test passed"
                """
            }
        }
    }

    // ── Post-pipeline Actions ──────────────────────────────────
    post {
        success {
            echo "Pipeline completed successfully for build ${BUILD_NUMBER}"
        }
        failure {
            echo "Pipeline FAILED. Rolling back..."
            withKubeConfig([credentialsId: "${KUBECONFIG_CRED}"]) {
                sh "kubectl rollout undo deployment/aceest-fitness --namespace=aceest"
            }
        }
        always {
            cleanWs()
        }
    }
}
