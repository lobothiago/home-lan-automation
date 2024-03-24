$wsl_ip_address = bash.exe -c "ifconfig eth0 | grep 'inet '"
$found = $wsl_ip_address -match '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}';

if ($found)
{
  $wsl_ip_address = $matches[0];
} else{
  echo "The Script Exited, the ip address of WSL 2 cannot be found";
  exit;
}

# All the ports you want to forward separated by coma
$ports=@(2375,2376);
$ports_a = $ports -join ",";

# Generic IPv4 address
$v4addresses=@('0.0.0.0');

# Fetch IPv6 addresses
$v6addresses = ipconfig.exe /all | Select-String -Pattern 'IPv6 Address' | Select-String -Pattern 'Temporary|Link-local' -NotMatch

# echo $v6addresses

for ($i = 0; $i -lt $v6addresses.length; $i++) 
{
  $current_address = $v6addresses[$i];
  $v6addresses[$i] = $current_address -replace '.*?IPv6.*?: (.*?)\(+.*', '$1';
}

# Setup port proxies (forwardings) for each port and each IPvX address
for ($i = 0; $i -lt $ports.length; $i++) 
{
  $port = $ports[$i];

  for ($j = 0; $j -lt $v4addresses.length; $j++) 
  {
    $address = $v4addresses[$j];
    iex "netsh interface portproxy delete v4tov4 listenport=$port listenaddress=$address";
  }
  
  for ($j = 0; $j -lt $v6addresses.length; $j++) 
  {
    $address = $v6addresses[$j];
    iex "netsh interface portproxy delete v6tov4 listenport=$port listenaddress=$address";
  }
}
