# Extragere profile din sistem
$profiles = netsh wlan show profiles | Select-String "All User Profile" | ForEach-Object { ($_ -split ":")[1].Trim() }

# Creare obiect pt stocarea datelor extrase din profile
$wifiDetails = @()

foreach ($profile in $profiles) {
    # Extragere date, setm show-password clear
    $details = netsh wlan show profile name="$profile" key=clear
    
    # Extrage parola din detalii
    $password = ($details | Select-String "Key Content" | ForEach-Object { ($_ -split ":")[1].Trim() })

    # Stocam numele si parola in clar in obiectul creat
    $wifiDetails += [PSCustomObject]@{
        SSID = $profile
        Password = $password
    }
}

# Afisam in consola
$wifiDetails | Format-Table -AutoSize

# Cream un csv file cu datele extrase
$wifiDetails | Export-Csv -Path "wifi_details.csv" -NoTypeInformation
