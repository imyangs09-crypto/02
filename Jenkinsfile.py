pipeline {
  agent {
    docker {
      image 'mcr.microsoft.com/playwright/python:v1.45.0-jammy'
      args  '-u root:root'  // 允许安装依赖
    }
  }
  options { timestamps(); ansiColor('xterm') }
  environment {
    PYTHONUNBUFFERED = '1'
    PLAYWRIGHT_HEADLESS = '1'  // 强制无界面
  }
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Install Deps') {
      steps {
        sh '''
          pip install -r requirements.txt
          playwright install --with-deps chromium firefox webkit
        '''
      }
    }
    stage('Tests (Parallel Browsers)') {
      steps {
        sh '''
          pytest -n auto \
            --browser chromium --browser firefox --browser webkit \
            --alluredir=allure-results \
            --junitxml=reports/junit.xml -s -v
        '''
      }
    }
    stage('Allure Report') {
      steps {
        sh 'allure generate allure-results -o allure-report --clean || true'
      }
    }
  }
  post {
    always {
      junit 'reports/junit.xml' // JUnit 测试趋势
      archiveArtifacts artifacts: 'allure-results/**', fingerprint: true
      archiveArtifacts artifacts: 'allure-report/**', fingerprint: true
    }
  }
}


