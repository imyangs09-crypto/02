// 最小可运行 Declarative Pipeline（不依赖 Docker/AnsiColor 插件）
pipeline {
  agent any
  options { timestamps() }     // 先别用 ansiColor
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Build') {
      steps {
        sh '''
          echo "Hello from Jenkins on $(uname -a)"
          # 在构建节点的系统 Python/工具中运行你的命令
        '''
      }
    }
  }
}

