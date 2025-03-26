        <?php
        include 'header.html';
            if (isset($_GET['p'])) {
                $post = $_GET['p'];
                $dziala = True;
                $postFixed = str_replace('_', ' ', $post);
                echo '<center> <br> <p class="h3 font-monospace fw-bold">' . $postFixed . '</p> <br> <br> </center>';
            } else {
                $dziala = False;
                echo '<center> <br> <br> <br> <p class="h3 font-monospace fw-bold">Prosze tu nie zaglądać!</p> <br> <br> <br> </center>';
            }

            $server = 'localhost';
            $user = 'root';
            $password = '123';
            $dbName = 'ogloszenia';

            $conn = new mysqli($server, $user, $password, $dbName);

            if ($conn->connect_error) {
                die("Connection failed: " . $conn->connect_error);
            }
            if ($dziala){
                $result = $conn->query("SHOW COLUMNS FROM `testowe` LIKE '$post'");

             if ($result->num_rows > 0) {
                     
                 $sql = "SELECT $post FROM testowe";
                 $result = $conn->query($sql);

                 if ($result) {
                     while ($row = $result->fetch_assoc()) {
                         echo '<center> <p class="h4 font-monospace">' . $row[$post] . "</p> </center> <br>";
                     }
                 } else {
                     echo "error";
                 }
             } else {
                 echo '<center> <br> <br> <br> <p class="h3 font-monospace fw-bold">A ty co panie haker!</p> <br> <br> <br> </center>';
             }	
            }

            $conn->close();
        include 'footer.html';
            ?>