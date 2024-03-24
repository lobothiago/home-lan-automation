# Remote UI Access Setup for Ubuntu Server with xRDP

To facilitate easy remote UI access to an Ubuntu server, it is recommended to use xRDP. This guide will walk you through the steps of installing xRDP, creating a dedicated user for RDP access, and configuring the necessary settings.

## Step 1: Install xRDP

Run the following command in the terminal to install xRDP:

```bash
sudo apt install xrdp
```

## Step 2: Create a Dedicated User for RDP Access

It is recommended to create a dedicated user for RDP access. This is because only one session can be active for a given user at a time. By having one user for physical access and another exclusively for RDP, you can avoid conflicts.

## Step 3: Configure .xsessionrc

In the home directory of the newly created XRDP user, you need to create a file named `.xsessionrc`. Add the following content to this file to ensure proper environment setup for the session:

```bash
export GNOME_SHELL_SESSION_MODE=ubuntu
export XDG_CURRENT_DESKTOP=ubuntu:GNOME
export XDG_CONFIG_DIRS=/etc/xdg/xdg-ubuntu:/etc/xdg
```
