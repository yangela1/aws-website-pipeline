# Documentation
## Overall Architecture

![Architecture image](https://aws-website-pipeline.s3.us-west-2.amazonaws.com/Assignment4Architecture.drawio.png)

- `index.html` retrieves image file from S3 bucket to display on the webpage 

## Pipeline Architecture
AWS CodePipeline to create CI/CD pipeline
1. **Source stage**: Monitors this Github repo for changes
2. **Build stage**: Builds and packages the website code
3. **Test stage**: Runs automated tests (using Selenium) on build artifact 
4. **Deploy stage**: Deploys the website to the DeploymentGroup (1 Linux EC2 instance)

## Steps to set up the pipeline
### Prerequisites
1.  Create a Github repo with website code
2. Create IAM Roles: 
- EC2 instance role: has `AmazonEC2RoleforAWSCodeDeploy` and `AmazonSSMManagedInstanceCore` policies
- CodeDeploy role: has `AWSCodeDeployRole` policy
3. Launch 1 Linux EC2 instance with EC2 instance role attached. Insert these commands into the User Data section.

```bash
#!/bin/bash
# Update all packages
yum update -y

# Install Ruby
yum install -y ruby

# Install the CodeDeploy Agent (replace region as needed)
cd /home/ec2-user
wget https://aws-codedeploy-us-west-2.s3.us-west-2.amazonaws.com/latest/install
chmod +x ./install
./install auto

# Start the CodeDeploy Agent
service codedeploy-agent start
```
* this installs ruby, the CodeDeploy agent into the EC2 instance, and starts it (needed for CodeDeploy stage)

### Step 1: Create AWS CodePipeline
- Give pipeline a name
- Create a new service role for pipeline
### Step 2: Source Stage (Github Integration)
- In Source provider, select `Github`
- Create a connection to GitHub account and select the repo and branch to monitor for changes
### Step 3: Build Stage (CodeBuild)
- Create a new Build Project in CodeBuild - Choose `Github` for Source, 
Linux env, attach a new Service role, in the buildspec.yml input the following commands (ensure the commands to install the webserver into the EC2 instance is within ./scripts/start_server.sh directory): 

```yml
version: 0.2
phases:
  build:
    commands:
      - echo "Building the website..."
      # Add any other build commands if needed (e.g., bundling, minifying)
      - chmod +x scripts/start_server.sh

artifacts:
  files:
    - '**/*'
```

* this gives execution privileges to start the httpd server on the EC2 instance

- Add Build stage to CodePipeline. Select `AWS CodeBuild` for Build provider and choose the newly created Build Project. Keep `SourceArtifact` default


### Step 4: Deploy Stage (Deploy to EC2 Deployment Group)
- Create a new Application.
- Within the Application, Create a Deployment Group. Select the configured EC2 Linux for Environment configuration and attach the `AWS CodeDeploy` role to allow it to receive deployments. Ensure `Load Balancing` is unchecked.

- Add Deploy stage to CodePipeline. Select `AWS CodeDeploy` for Deploy provider. Choose the newly created Application and Deployment Group. Ensure the EC2 instance has permissions and an agent running for CodeDeploy. In the repository include `appspec.yml` file that defines how files are deployed to the instance.

### Step 5: Finalize and Review Pipeline
- Ensure each stage (Source, Build, Test, Deploy) is correctly configured.
- Create the pipeline. It will automatically start and rebuild everytime any changes are detected from the Github repo

### Step 6: View the deployed website
- Select the `Instance Id` from Deploy stage. Copy the public IPv4 address of the EC2 instance into the browser

### Optional Step:  Test Stage (CodeBuild)
- This step is for creating an automated testing stage that tests your code before deployment using Selenium 
- Create a new Test Project - Choose `GitHub` for Source, Linux env, attach a new Service role, in the `buildspec.yml` input the following commands to run the test script (ensure the script is in the ./scripts./test_selenium.py directory): 

```yml
version: 0.2

phases:
  install:
    commands:
      - echo "Installing dependencies..."

      # Install wget, unzip, python3, pip3
      - sudo yum install -y wget unzip python3 python3-pip

      # Install Google Chrome
      - wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
      - sudo yum localinstall -y google-chrome-stable_current_x86_64.rpm

      # Install ChromeDriver version 130.0.6723.116
      - wget https://storage.googleapis.com/chrome-for-testing-public/130.0.6723.116/linux64/chrome-linux64.zip
      - unzip chrome-linux64.zip

      # Install Selenium
      - pip3 install selenium

  build:
    commands:
      - echo "Running Selenium tests..."
      - export CHROME_BIN=$(pwd)/chrome-linux64/chrome  # Set the chrome binary path
      - python3 ./scripts/test_selenium.py  # Ensure this script exists in your repository

artifacts:
  files:
    - '**/*'  # Optionally, specify files if you need to store logs or reports

```
* this installs Google Chrome, Python, ChromeDriver, Selenium and runs the script

- Add Test stage to CodePipeline in between the Build and Deploy stages. Select `Add Stage`, `Add action group`,  select `AWS CodeBuild` for Action provider. Select `BuildArtifact` for Input artifacts and choose the newly created Test Project for Project Name.

- Save changes the click `Release change` to deploy updated pipeline

## Maintaining and Debugging
- Use the Pipeline details page to monitor stages
- Check logs in CloudWatch or within the details popup if any issues arrise during CodeBuild or CodeDeploy stages 
- Source: Ensure the correct Github repo is selected 
- Build: Ensure each CodeBuild project has its own `buildspec.yml` and has the correct input artifacts (the Test Stage requires the `BuildArtifact` from the Build stage for testing)
- Deploy: Ensure the repo has an `appspec.yml file`, the EC2 instance has all required dependencies installed (ruby, CodeDeploy agent) within User Data section. To check if the CodeDeploy agent is running, SSH into the EC2 and do `sudo service codedeploy-agent status`.
- Test: View the logs to see testing information
