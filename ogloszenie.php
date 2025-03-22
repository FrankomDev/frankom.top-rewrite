<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>wasil network</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <link rel="stylesheet" href="style.css">
</head>
<body>
        <center>
        <img src="img/logo.png">
        </center>
        <div class="container-xs p-3 bg-danger border border-5 border-dark border-dashed" style="border-style: dashed !important;">
            <div class="btn-group-lg">
                <center>
                <a href="/">
                <button type="button" class="btn font-monospace fw-bold">Strona główna</button>
                </a>
                <a href="/rometzxt.html">
                <button type="button" class="btn font-monospace fw-bold">Romet ZXT</button>
                </a>
                <a href="/sprzet.html">
                <button type="button" class="btn font-monospace fw-bold">Sprzęt</button>
                </a>
                <a href="/ogloszenia.php">
                <button type="button" class="btn font-monospace fw-bold">Ogłoszenia</button>
                </a>
                <a href="/kontakt.html">
                <button type="button" class="btn font-monospace fw-bold">Kontakt</button>
                </a>
                </center>
            </div>
        </div>

        <div class="container-xs p-3 bg-danger border border-5 border-dark border-dashed mt-2" style="border-style: dashed !important;">
            
        <?php
            if (isset($_GET['p'])) {
                $post = $_GET['p'];
                $dziala = True;
                echo '<center> <br> <p class="h3 font-monospace fw-bold">' . $post . '</p> <br> <br> </center>';
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
            ?>
        </div>

        <div class="container-xs p-3 bg-danger border border-5 border-dark border-dashed mt-2" style="border-style: dashed !important;">
            <div class="d-flex justify-content-between align-items-center">
                <img src="gifs/ziolo.gif">
                <p class="h5 fw-bold font-monospace">wasil network sp. z. o. o</p>
                <img src="gifs/ziolo.gif">
            </div>
            <div class="line">
            <center>
            <img src="gifs/line.gif">
            </center>
            </div>
            
        </div>

</body>
</html>