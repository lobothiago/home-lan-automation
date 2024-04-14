# Remote Hibernation in Windows

This guide outlines the steps to set up remote hibernation on a Windows machine, allowing you to remotely hibernate your computer.

## Step 1: Installation

First, download and install the necessary software from the following sources:

- [Remote Shutdown PC v1.1.16](https://github.com/karpach/remote-shutdown-pc/releases/tag/v1.1.16) - Direct download link also available at `resources/software/remote-shutdown-pc.zip`.

## Step 2: Configuration

After installing the software, you need to configure it to suit your needs.

![Windows Remote Shutdown Configuration](https://github.com/lobothiago/home-lan-automation/blob/main/resources/images/windows-remote-shutdown-config.png?raw=true)

- Choose a **secret code** as necessary for secure operations.

## Step 3: Create a Scheduled Startup Task

Follow the instructions provided in `notes/windows-ssh-access` to create a scheduled task for starting up your computer remotely.

### 3.1 Task Action Configuration

When configuring the action for the scheduled task, use the settings as shown in the image below:

![Scheduled Task Action for Windows Remote Shutdown](https://github.com/lobothiago/home-lan-automation/blob/main/resources/images/windows-remote-shutdown-scheduled-task-action.png?raw=true)
