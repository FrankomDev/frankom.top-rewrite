
<?php

require '/usr/share/php/Dotenv/autoload.php';
$dotenv = Dotenv\Dotenv::createImmutable(__DIR__);
$dotenv->load();

include 'header.html';
            echo '<center>
            <br>
            <p class="h3 font-monospace fw-bold">Ogłoszenia</p>
            <br>
            <img src="gifs/user.gif" class="float-end">
            </center>';

            $server = $_ENV['server'];
            $user = $_ENV['user'];
            $password = $_ENV['password'];
            $dbName = $_ENV['dbName'];

            $conn = new mysqli($server, $user, $password, $dbName);

            if ($conn->connect_error) {
                die("Connection failed: " . $conn->connect_error);
            }

            $sql = "SHOW COLUMNS FROM testowe";
            $result = $conn->query($sql);

            if ($result->num_rows > 0) {
                while ($row = $result->fetch_assoc()) {
                    $rowFieldFixed = str_replace('_', ' ', $row['Field']);
                    echo '<a href=ogloszenie.php?p=' . $row['Field'] . '>' . '<p class="h4 font-monospace fw-bold">' . $rowFieldFixed . "</p> </a> <br>";
                }
            } else {
                echo "<center> <p class=h4 font-monospace fw-bold>Brak postów</p> </center>";
            }


            $conn->close();
            echo '<br>
            <center>
                <img src="gifs/banner.gif" id="logo">
            </center>';

        include 'footer.html'
            ?>