<?php header("Access-Control-Allow-Origin: *");
//header('Content-Type: application/json');
    $start_time = $_GET['start_time'];
    $end_time = $_GET['end_time'];
    $LIMIT = $_GET['LIMIT'];
    $data = [["word"=>"Hello","num"=>10],["word"=>"Hi","num"=>2],["word"=>"Yes","num"=>5]];
    header('Content-type: application/json');
    echo json_encode( $data );
?>
