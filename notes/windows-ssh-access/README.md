# SSH Access to WSL2 in Windows

Follow these steps to set up SSH access to WSL2 on Windows. This guide includes creating scheduled tasks for NAT workaround and starting the SSH daemon.

## 1. Install WSL2

First, ensure WSL2 is installed on your system. If not, follow Microsoft's guide to install WSL2.

## 2. Deploy NAT Workaround Script

Next, you need to deploy the NAT workaround script.

- Deploy `scripts/windows/wsl2_nat_workaround.ps1` to your desired `<path>`.

## 3. Create New Scheduled Task for the NAT Workaround Script

This task will ensure the NAT workaround script runs at system startup.

### 3.1 Change User or Group

- Go to the "General" tab in the new scheduled task window.
- Click "Change User or Group".

### 3.2 Advanced

- Select "Advanced".

### 3.3 Find Now

- Click "Find Now".

### 3.4 Choose Users

- In the search results, select "Users".
- Click "OK" > "OK".

![](https://github.com/lobothiago/home-lan-automation/blob/main/resources/images/scheduled-task-user-picking.png?raw=true)

### 3.5 Run with Highest Privileges

- Check the option "Run with highest privileges".

![](https://github.com/lobothiago/home-lan-automation/blob/main/resources/images/scheduled-task-general-tab.png?raw=true)

### 3.6 Triggers Tab > New > At Startup

- Switch to the "Triggers" tab.
- Click "New".
- Set the trigger to "At startup".

![](https://github.com/lobothiago/home-lan-automation/blob/main/resources/images/scheduled-task-triggers-tab.png?raw=true)

### 3.7 Actions Tab > New > Start a Program

- Switch to the "Actions" tab.
- Click "New".

### 3.8 Program/Script

- Set Program/Script to `PowerShell.exe`.

### 3.9 Add Arguments

- In "Add arguments", enter your `<path>` to the `wsl2_nat_workaround.ps1` script.

![](https://github.com/lobothiago/home-lan-automation/blob/main/resources/images/scheduled-task-actions-tab.png?raw=true)

## 4. Create New Scheduled Task to Enable `sshd` in WSL2

This task will start the SSH daemon within WSL2 at startup.

### 4.1 Change User or Group

- Similar to step 3.1.

### 4.2 Advanced

- Similar to step 3.2.

### 4.3 Find Now

- Similar to step 3.3.

### 4.4 Choose Users

- Similar to step 3.4.

### 4.5 Run with Highest Privileges

- Similar to step 3.5.

### 4.6 Triggers Tab > New > At Startup

- Similar to step 3.6.

### 4.7 Actions Tab > New > Start a Program

- Similar to step 3.7.

### 4.8 Program/Script

- Set Program/Script to `bash.exe`.

### 4.9 Add Arguments

- In "Add arguments", enter `-c "sudo service ssh start"`.

## 5. Enable All Tasks History

- On the main Task Scheduler screen, make sure to enable all tasks history to keep track of task executions.

![](https://github.com/lobothiago/home-lan-automation/blob/main/resources/images/task-scheduler-enable-all-tasks-history.png?raw=true)
