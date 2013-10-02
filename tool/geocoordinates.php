<?php
require_once(dirname(__FILE__).'/lib/functions.php');
require_once(dirname(__FILE__).'/geoconfig.php');


$x = 332;
$y = 49;
$geoCoordinates = getGeoCoordinates($config,$x,$y);
print_r($geoCoordinates);



// // move temple coordinats to right hand coordinate system
// foreach ($temple as $coordinate) {
// 	$templeCoords[] = moveToRightHandSystem($coordinate['x'], $coordinate['y'],$maxY);
// }

// // set the right hand temple coordinates
// $templeCoordinates = array(
// 		'x1' => $templeCoords[0]['x'],
// 		'y1' => $templeCoords[0]['y'], 
// 		'x2' => $templeCoords[1]['x'], 
// 		'y2' => $templeCoords[1]['y']
// 		);

// // calculate the radians of the rotation
// $radians = -1 * calculateAngle($hypotenuse);

// // rotate the geoCoordinates to the Y axis
// $geoCoordinates = rotateToAxis($hypotenuse,$center,$geoTemple);

// // set the rotated temple coordinates
// $newGeoCoordinates = array(
// 		// lower left corner
// 		'x1' => $geoCoordinates[0]['x'],
// 		'y1' => $geoCoordinates[0]['y'],
// 		// upper right corner
// 		'x2' => $geoCoordinates[3]['x'],
// 		'y2' => $geoCoordinates[3]['y']
// 		);

// $x = 114;
// $y = 534.03;
// $extent = array('x' => 5.81, 'y' => 11.25);

// $movedOldCoordinates = moveToRightHandSystem($x, $y, $maxY);

// $newCoordinates = transformCoords($newGeoCoordinates,$templeCoordinates, $movedOldCoordinates['x'], $movedOldCoordinates['y'], 12);
// // $newExtent = transformExtent($newGeoCoordinates, $templeCoordinates, $extent, 12);
// // print_r($newExtent);

// // center point for rotation (left bottom side of building)
// // $center = array('x'=>32.873111, 'y'=>24.977378);

// $finalCoordinates = rotatePoint($newCoordinates['x'],$newCoordinates['y'],$center,$radians);
// print_r($finalCoordinates);


// // $polygon = array(
// // 	array(
// // 		'x' => $finalCoordinates['x'],
// // 		'y' => $finalCoordinates['y'] - $newExtent['y'],
// // 		),
// // 	array(
// // 		'x' => $finalCoordinates['x'],
// // 		'y' => $finalCoordinates['y'] + $newExtent['y'],
// // 		),
// // 	);

// // print_r($polygon);
?>