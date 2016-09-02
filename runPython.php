<?php
	$start = microtime(true);
	$var = 'akanksharedhu';
	$file = './scrapInsta.py';
	$cmd = $file . ' ' . $var;
	$command = escapeshellcmd($cmd);
	$output = shell_exec($command);
	str_replace('\n', '', $output);
	$output = (string)$output;
	$user = json_decode($output,true);
	// $user = json_decode($user);
	// $user = json_decode($user);
	print_r($user);
	// print(microtime(true) - $start);

?>