## Customizing GRUB to Fetch Default Option from TFTP Server

To configure GRUB to load its default boot option from a TFTP server, follow these steps:

### 1. Configure Motherboard for Network Initialization

Ensure that the motherboard is set to initialize the network stack on boot. This is usually achieved by enabling a feature similar to "PXE booting" in the BIOS settings.

### 2. Edit GRUB Configuration

On the operating system that manages GRUB, perform the following steps:

- Edit the GRUB custom script file located at `/etc/grub.d/40_custom` by adding the following lines:

```bash
insmod net
insmod efinet
insmod tftp
net_bootp
source (tftp,<tftp_server_ip_NOT_HOSTNAME>)/grub_conf
```

Replace `<tftp_server_ip_NOT_HOSTNAME>` with the actual IP address of your TFTP server.

### 3. Update GRUB Configuration

After editing the GRUB configuration, update GRUB by running the following command in the terminal:

```shell
sudo update-grub
```