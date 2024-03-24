# TFTPD Installation and Configuration in Raspberry PI

Follow these steps to install and configure TFTPD on your Raspberry Pi:

## 1. Install TFTPD

```bash
sudo apt install tftpd-hpa
```

## 2. Create Firewall Rule to Allow Access

```bash
sudo ufw allow 69 comment 'tftp'
```

## 3. Make /tftp Globally Readable and Writable

```bash
chmod -R 777 /tftp
```

## 4. Adjust Service Configuration

Edit the `/etc/default/tftpd-hpa` file with the following content:

```plaintext
# /etc/default/tftpd-hpa

TFTP_USERNAME="tftp"
TFTP_DIRECTORY="/tftp"
TFTP_ADDRESS=":69"
TFTP_OPTIONS="--verbosity 1 --ipv4 --secure --create"
RUN_DAEMON="yes"
```

## 5. Restart the Service

```bash
sudo service tftpd-hpa restart
```

## 6. Validate Access from Another Machine

### 6.1 Add Dummy File to TFTP Directory

```bash
echo "123" > /tftp/test.txt
```

### 6.2 Access Server from Another Machine and Download Dummy File

```bash
tftp <server_ip>
get test.txt
```
