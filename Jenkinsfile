pipeline {
  agent any
  options { timestamps() }
  stages {
    stage('Checkout'){ steps { checkout scm } }
    stage('Setup venv') {
      steps {
        sh '''
          python3 -m venv .venv
          . .venv/bin/activate
          python -m pip install --upgrade pip
          pip install "numpy<2" pytest playwright
          playwright install --with-deps
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

