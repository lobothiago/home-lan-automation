SSH Access to WSL2 in Windows

1 - Install WSL2
2 - Deploy scripts/windows/wsl2_nat_workaround.ps1 to desired <path>

3 - Create new scheduled task in Task Scheduler for the NAT workaround script
3.1 - Change user or group
3.2 - Advanced
3.3 - Find now
3.4 - Choose Users > OK > OK
![Test](https://github.com/lobothiago/home-lan-automation/blob/main/resources/images/scheduled-task-user-picking.png?raw=true)
3.5 - Check "Run with highest privileges"
3.6 - Triggers Tab > New > At startup
3.7 - Actions Tab > New > Start a Program
3.8 - Program/Script: PowerShell.exe 
3.9 - Add arguments: "<path>"

4 - Create new scheduled task in Task Scheduler to enable sshd in WSL2
4.1 - Change user or group
4.2 - Advanced
4.3 - Find now
4.4 - Choose Users > OK > OK
4.5 - Check "Run with highest privileges"
4.6 - Triggers Tab > New > At startup
4.7 - Actions Tab > New > Start a Program
4.8 - Program/Script: bash.exe
4.9 - Add arguments: -c "sudo service ssh start"

5 - On main Task Scheduler screen: Enable all tasks history