<?php

// number of decimal places
const NUMBERTAIL = 12;

$config = array(
	// temple coordinates (without pylon) (rectangle in axis)
	'temple' => array(
			// lower left corner
			array(
				'x' => 114,
				'y' => 716
			),
			// upper right corner
			array(
				'x' => 369,
				'y' => 13
			),
		),
	// height of the image (necessary to move the image to right hand coordinate system)
	'maxY' => 900,
	// geocoordinates of the temple (without pylon) in decimal degree (rectangle not in axis)
	'geoTemple' => array(
			// lower left corner
			array(
				'x' => 32.873219,
				'y' => 24.977478
			),
			// upper left corner
			array(
				'x' => 32.873264,
				'y' => 24.978622
			),
			// lower right corner
			array(
				'x' => 32.873689,
				'y' => 24.977461
			),
			// upper right corner
			array(
				'x' => 32.873739,
				'y' => 24.978608
			),
		),
	// the hypotenuse, in this case the lower left and upper left coordinates
	'hypotenuse' => "32.873219,24.977478,32.873264,24.978622",
	// the rotation point, here the lower left corner
	'center' => array(
				'x' => 32.873219,
				'y' => 24.977478
			)
	);
?>