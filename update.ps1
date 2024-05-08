if (-Not (Get-Command 'py' -errorAction SilentlyContinue)) {
	$yn = Read-Host "Python is not installed. You must install Python to use the Manifest Manager. Install it now? [Y/n] "
	$yn = $yn.ToLower()
	if ($yn -ne "n") {
		Write-Output "Downloading installer..."
		[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
		Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe" -OutFile ".\python-3.12.3.exe"
		Write-Output "Installing Python. Please re-run the installer once completed by running .\update.ps1"
		Read-Host "Press Enter to continue."
		.\python-3.12.3.exe InstallAllUsers=0 PrependPath=1 Include_test=0 TargetDir=C:\Python\Python312

		Remove-Item .\python-3.9.0.exe -Force 2>$null
		Write-Output "Installing Python modules..."
		py -m pip install -r requirements.txt
		Read-Host "Installation complete. Press Enter to continue to continue to Manifest Manager."

		setx path "%PATH%;C:\Python\Python312\"
		Set-Variable "path=%PATH%;C:\Python\Python312\"

		py manifest-manager.py

		<#
		$compress = @{
			Path             = ".\overrides", ".\manifest.json", ".\manifest-manager.py", ".\modlist.html", ".\update.ps1"
			CompressionLevel = "Fastest"
			DestinationPath  = ".\THIS_ONE.zip"
		}
		
		Compress-Archive @compress
		#>

	}
	else {
		Write-Output "Please install Python https://python.org"
		Read-Host "Press Enter to continue."
	}
}
else {
	py manifest-manager.py
}