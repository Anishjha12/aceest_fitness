pipeline {
    agent any

    environment {
        APP_NAME        = "aceest-fitness"
        DOCKER_REGISTRY = "docker.io"
        DOCKER_IMAGE    = "anishjha12/aceest-fitness"
        IMAGE_TAG       = "${BUILD_NUMBER}"
        SONAR_PROJECT   = "aceest-fitness"
        KUBECONFIG_CRED = "kubeconfig-credentials"
        GITHUB_REPO     = "https://github.com/Anishjha12/aceest_fitness"
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
        bat """
            python -m pip install --upgrade pip
            pip install -r requirements.txt
        """
    }
}

        // ── 3. Unit Tests + Coverage ───────────────────────────
stage("Unit Tests") {
    steps {
        bat """
            set PYTHONPATH=%CD%
            pytest tests/ --cov=app --cov-report=xml:coverage.xml --cov-report=html:htmlcov --junitxml=test-results.xml -v
        """
    }
    post {
        always {
            junit "test-results.xml"
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
            script {
                def scannerHome = tool "SonarScanner"
                bat """
                    "${scannerHome}\\bin\\sonar-scanner.bat" ^
                        -Dsonar.projectKey=%SONAR_PROJECT% ^
                        -Dsonar.projectName="ACEest Fitness" ^
                        -Dsonar.sources=app ^
                        -Dsonar.tests=tests ^
                        -Dsonar.python.coverage.reportPaths=coverage.xml ^
                        -Dsonar.python.version=3.11
                """
            }
        }
    }
}

        // ── 5. Quality Gate ────────────────────────────────────
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
                bat "docker build -t %DOCKER_IMAGE%:%IMAGE_TAG% ."
                bat "docker tag %DOCKER_IMAGE%:%IMAGE_TAG% %DOCKER_IMAGE%:latest"
                echo "Docker image built: ${DOCKER_IMAGE}:${IMAGE_TAG}"
            }
        }

        // ── 7. Push to Docker Hub ──────────────────────────────
        stage("Push Docker Image") {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "dockerhub-credentials",
                    usernameVariable: "DOCKER_USER",
                    passwordVariable: "DOCKER_PASS"
                )]) {
                    bat """
                        docker login -u %DOCKER_USER% -p %DOCKER_PASS%
                        docker push %DOCKER_IMAGE%:%IMAGE_TAG%
                        docker push %DOCKER_IMAGE%:latest
                    """
                }
                echo "Image pushed to Docker Hub"
            }
        }

        // ── 8. Deploy to Kubernetes ────────────────────────────
        stage("Deploy - Rolling Update") {
            steps {
                withKubeConfig([credentialsId: "${KUBECONFIG_CRED}"]) {
                    bat """
                        kubectl apply -f k8s/deployment.yaml
                        kubectl set image deployment/aceest-fitness aceest-fitness=%DOCKER_IMAGE%:%IMAGE_TAG% --namespace=aceest
                        kubectl rollout status deployment/aceest-fitness --namespace=aceest
                    """
                }
            }
        }

        // ── 9. Smoke Test ──────────────────────────────────────
        stage("Smoke Test") {
            steps {
                bat """
                    timeout /t 10 /nobreak
                    curl -f http://localhost:5000/ || exit 1
                    echo Smoke test passed
                """
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully for build ${BUILD_NUMBER}"
        }
        failure {
            echo "Pipeline FAILED for build ${BUILD_NUMBER}"
        }
        always {
            cleanWs()
        }
    }
}