pipeline {
  agent any
  options { timestamps() }
  stages {
    stage('Checkout'){ steps { checkout scm } }
stage('Setup venv') {
  steps {
    sh '''
      set -eux
      python3 -m venv .venv
      . .venv/bin/activate
      python -m pip install --upgrade pip
      pip install "numpy<2" pytest
      # 如需 Playwright：
      pip install playwright pytest-playwright
      python -m playwright install  # 先不带 --with-deps，避免需要 apt 权限
    '''
  }
}
    stage('Test') {
      steps {
        sh '''
          . .venv/bin/activate
          pytest -s -v
        '''
      }
    }
  }
  post { always { archiveArtifacts artifacts: '**/test-results*/**/*, **/playwright-report/**', fingerprint: true } }
}

