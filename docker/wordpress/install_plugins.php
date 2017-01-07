<?php

/** @var array $plugins */
$plugins = json_decode(file_get_contents('/var/www/wordpress/plugins.json'), true);

if (is_array($plugins)) {
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36");
    curl_setopt($curl, CURLOPT_FOLLOWLOCATION, true);
    foreach ($plugins as $plugin) {
        if (is_array($plugin)) {
            foreach ($plugin as $version => $info) {
                $zip  = $info['zip'];
                $file = fopen('/tmp/plugin.zip', 'w+');
                curl_setopt($curl, CURLOPT_URL, $zip);
                curl_setopt($curl, CURLOPT_FILE, $file);
                curl_exec($curl);
                fclose($file);
                exec('unzip /tmp/plugin.zip -d /var/www/wordpress/wp-content/plugins/');
            }
        }
    }
    curl_close($curl);
}
