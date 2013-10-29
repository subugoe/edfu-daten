<?php
require_once(dirname(__FILE__).'/simple_html_dom.php');

/**
 * Main program for scraping images and
 * Fetches an URL and the nested image maps and areas or areas from a gif-file.
 * Relevant informations from the areas are read and calculated. 
 * 
 * @param  $room  an array with room informations
 * @param  $lists an array of lists with specific exceptions
 * @return the data for each area
 */
function run($room,$lists) {
	$type = pathinfo($room['url'],PATHINFO_EXTENSION);
	$i = 0;
	$go = true;
	if ($type == 'html') {
		$site = file_get_html($room['url']);
		$href = array();
		$imageMaps = checkForImageMaps($site);
	}
	if ($type == 'gif') {
		$areas = findAreasFromImage($room['url'],array(2,0),1,$room['cut']);
		if (isset($room['onlyWhite'])) {
			//only white areas:
			$areas = findAreasFromImage($room['url'],array(0),1,$room['cut']);	
		}
		
		
	}
	if ($type == 'gif' || $areas = checkForAreas($site)) {
		foreach($areas as $area) {
			if ($type == 'gif' || $area->href) {
				if ($type == 'html') {
					$parts = preg_split("/Edfou|, p. |, \(pl. /", $area->title);
					@$data[$i] = array('description' => rtrim(trim(html_entity_decode($parts[0])),' -'),
									'volume' => trim($parts[1]),
									'page' => trim($parts[2]),
									'plate' => trim($parts[3],')'),
									'polygon' => $area->coords,
									'link' => $area->href,
								);
				}
				if ($type == 'gif') {
					$areaString = coordsToString($area);
					$data[$i] = array('description' => '',
						'volume' => '',
						'page' => '',
						'plate' => '',
						'polygon' => $areaString,
						'areacolor' => $area['color'],
						'link' => '',
					);
					unset($area['color']);
				}

				// checks a list with areas that cannot be calculated with the calculation tool
				foreach ($lists['exceptionList'] as $exception) {
					if ($data[$i]['link'] == $exception || $data[$i]['polygon'] == $exception)
						$go = false;
				}
				if ($go) {
					$itsAPolygon = false;
					$areaString = $data[$i]['polygon'];
					echo "areaString is $areaString ";
					$areaCoords = defineCoords($areaString);
					if (!$areaCoords) {
						$areaCoords = createRectangleFromPolygon($areaString);
						$areaCoords = defineCoords($areaCoords);
						$itsAPolygon = true;
					}
					$areaString = coordsToString($areaCoords);
					$correctWall = checkPosition($room['walls'], $areaString);

					// only necessary for polygon areas instead of rectangle
					if ($itsAPolygon) {
						echo " und das ist ein Polygon";
						$areaCoords = fitRectangleToWall($areaString, $lists['smallWallsList'],$correctWall);
						$areaString = coordsToString($areaCoords);
						$correctWall = checkPosition($room['walls'], $areaString);
						$data[$i]['polygon'] = $areaString;
						echo " und wird somit zu $areaString";
					}
					$data[$i] = array_merge($data[$i], calculate($areaString,$data[$i]['link'],$correctWall,$room['area'],$room['mainArea'],$lists['angleOfViewList'],$room['setting'],true));
					echo "<br>";
				}
				$go = true;	
				$i++;
			}
		}
	}
	return $data;
}


/**
 * Main program for calculating the geo coordinates of an specific coordinate
 * 
 * @param  $config the config array
 * @param  $x      x-coordinate
 * @param  $y      y-coordinate
 * @return the geo coordinates
 */
function getGeoCoordinates($config, $x, $y)
{
	// move temple coordinats to right hand coordinate system
	foreach ($config['temple'] as $coordinate) {
		$templeCoords[] = moveToRightHandSystem($coordinate['x'], $coordinate['y'],$config['maxY']);
	}

	// set the right hand temple coordinates
	$templeCoordinates = array(
			'x1' => $templeCoords[0]['x'],
			'y1' => $templeCoords[0]['y'], 
			'x2' => $templeCoords[1]['x'], 
			'y2' => $templeCoords[1]['y']
			);

	// calculate the radians of the rotation
	$radians = -1 * calculateAngle($config['hypotenuse']);

	// rotate the geoCoordinates to the Y axis
	$geoCoordinates = rotateToAxis($config['hypotenuse'],$config['center'],$config['geoTemple']);

	// set the rotated temple coordinates
	$newGeoCoordinates = array(
			// lower left corner
			'x1' => $geoCoordinates[0]['x'],
			'y1' => $geoCoordinates[0]['y'],
			// upper right corner
			'x2' => $geoCoordinates[3]['x'],
			'y2' => $geoCoordinates[3]['y']
			);
	// move coordindates to right hand system
	$movedCoordinates = moveToRightHandSystem($x, $y, $config['maxY']);
	// transform the right-hand coordinates to geocoordinates
	$newCoordinates = transformCoords($newGeoCoordinates,$templeCoordinates, $movedCoordinates['x'], $movedCoordinates['y'], NUMBERTAIL);
	// rotate the geocoordinates back to given angle
	$finalCoordinates = rotatePoint($newCoordinates['x'],$newCoordinates['y'],$config['center'],$radians);
	$finalCoordinatesString = $newCoordinates['y'] . ',' . $newCoordinates['x'];
	return $finalCoordinatesString;
}

/**
 * A simple logger
 * 
 * @param $text text output
 * @param $status status output e.g. WARNING, ERROR
 * @param $verbose set true if messages should only be shown in verbose mode
 */
function stdOut($text, $status = "", $verbose = false) {

    global $verboseOutputMode;
    if ((!$verboseOutputMode) && $verbose) {
        return;
    }
    //$time = date('y-m-d H:i:s', time());
    //echo nl2br("<" . $time . "> " . $status . " " . $text . "\n");
    echo nl2br($status . " " . $text . "\n");
}

/**
 * Checks if an array is an associative array
 * 
 * @param  $array 	an array
 * @return 
 */
function arrayIsAssoc($array) {
    foreach (array_keys($array) as $ind => $key) {
        if (!is_numeric($key) || (isset($array[$ind + 1]) && $array[$ind + 1] != $key + 1)) {
            return true;
        }
    }
    return false;
}

/**
 * Creates a csv file with the given data
 * 
 * @param  $data     the array with the relevant data
 * @param  $fileName name of file
 * @return 
 */
function createCsv($data,$fileName)
{
	$file = fopen($fileName, 'w');
    if (!$file)
        return false;

    if (arrayIsAssoc($data[0])) {
    	$captions = array_keys($data[0]);
  		array_unshift($data,$captions);
    }

	foreach ($data as $fields) {
    	fputcsv($file, $fields,";");
	}
	fclose($file);
	return true;
}

/**
 * Defines an array of coords including the smallest and biggest coordinates of an
 * rectangle (2 coordinates)
 * 
 * @param  $coords coords (as string (x1,y1,x2,y2 or as an array))
 * @return the defined coordinates
 */
function defineCoords($coords) {
	if (is_string($coords)) {
		$coordString = preg_replace('/ /', '', $coords);
		$coords = explode(',', $coordString);
	}
	if (count($coords)>4) {
		return false;
	}
	$fields = array('x1','y1','x2','y2');
	$coords = array_combine ($fields, $coords);
	$coords['minX'] = min($coords['x1'],$coords['x2']);
	$coords['maxX'] = max($coords['x1'],$coords['x2']);
	$coords['minY'] = min($coords['y1'],$coords['y2']);
	$coords['maxY'] = max($coords['y1'],$coords['y2']);
	return $coords;
}

/**
 * Converts an coordinate-array into a string
 * 
 * @param  $coords 	 coordinates
 * @return formatted comma seperated string
 */
function coordsToString($coords)
{
	$coords = array_slice($coords, 0, 4);
	$coordString = implode(',', $coords);

	return $coordString;
}

/**
 * Rotates the coordinates of an imagemap
 * 
 * @param  $coordString 	the coordinates of an area in the imagemap 
 * @param  $pictureWidth 	the width of the image-map picture
 * @return the rotated coordinates
 */
function rotateMapCoordsRight($coordString, $pictureWidth) {
	$coords = defineCoords($coordString);
	$newCoords['x1'] = $pictureWidth - $coords['y1'];
	$newCoords['y1'] = $coords['x1'];
	$newCoords['x2'] = $pictureWidth - $coords['y2'];
	$newCoords['y2'] = $coords['x2'];
	$coordString = implode(',', $newCoords);
	return $coordString;
}

/**
 * rotates the html imagemap to the right including all coordinates
 * 
 * @param  $url          	the url of the imagemap (html)
 * @param  $pictureWidth 	the width of the underlying picture
 * @return 
 */
function rotateMapRight($url, $pictureWidth) {
	$site = file_get_html($url);
	if ($imageMaps = checkForImageMaps($site)) {			
		foreach ($imageMaps as $imageMap) {
			if ($areas = checkForAreas($site)) {
				foreach($areas as $area) {
					$coordString = $area->coords;
					$newCoord = rotateMapCoordsRight($coordString, $pictureWidth);
					//stdOut("Old Coords were: $coordString, New Coords are: $newCoord","");
					$area->coords = $newCoord;	
				}
			}
		}
	}
	$site->save('map_right.html');
}

/**
 * A little helper function, which calculates the missing coordinates of walls
 * not needed for the script, but can speed up the definition of the wall rectangles
 * 
 * @param  $area          the innerlying area
 * @param  $missingCoords an array with the maximum coordinates of the north,east,south and west wall 
 * @return the missing wall coordinates
 */
function giveWallCoords($area,$missingCoords)
{
	$areaCoords = defineCoords($area);
	$walls = array('north' => array(
						$areaCoords['minX'], 
						$missingCoords[0], 
						$areaCoords['maxX'], 
						$areaCoords['minY']
						),
					'east' => array(
						$areaCoords['maxX'],
					 	$areaCoords['minY'],
					  	$missingCoords[1],
					   	$areaCoords['maxY']
					   	),
					'south' => array(
						$areaCoords['minX'],
						$areaCoords['maxY'],
						$areaCoords['maxX'],
						$missingCoords[2]
						),
					'west' => array(
						$missingCoords[3],
						$areaCoords['minY'],
						$areaCoords['minX'],
						$areaCoords['maxY']
						),
					);
	return $walls;
}

/**
 * Modifies a polygon into a maxed sized rectangle, so it can be used with the script
 * Used for polygons from the html imagemaps, not with images
 * 
 * @param  $polyongString string of an imagemap polygon
 * @return a string with the rectangle-coordinates     
 */
function createRectangleFromPolygon($polygonString)
{
	$polygonString = preg_replace('/ /', '', $polygonString);
	$polygon = explode(',', $polygonString);

	for ($i=0;$i<count($polygon);$i++) {
		// check if polygon coord is on first, third, etc position
		$keys = array_keys($polygon);
		if($keys[$i] % 2 == 0) {
			$x[] = $polygon[$i];
		}
		// otherwise its on second etc position, so it is the y coordinate
		else {
			$y[] = $polygon[$i];
		}
	}
	// sort and delete all but the smallest and biggest coordinate
	asort($x);
	asort($y);
	array_splice($x, 1, -1);
	array_splice($y, 1, -1);
	//build a string with the rectangle coordinates
	$coordsString = $x[0] . ',' . $y[0] . ',' . $x[1] . ',' . $y[1];
	return $coordsString;
}

/**
 * Shrink the rectangle which was created from a Polygon to fit the size of the wall
 * 
 * @param  $areaString 	the rectangle which was created from a polygon
 * @param  $smallWalls 	an array from the config file with the predefined walls 
 * @param  $wall 		the wall in which the rectangle lies
 * @return the smaller rectangle coordinates
 */
function fitRectangleToWall($areaString, $smallWalls, $wall)
{
	$area = defineCoords($areaString);
		foreach ($smallWalls as $key => $smallWall) {
			$smallWallCoords = defineCoords($smallWall);
			if ($wall == $key) {
				if ($area['x1']<$smallWallCoords['minX'])
					$area['x1'] = $area['minX'] = $smallWallCoords['minX'];
				if ($area['x2']<$smallWallCoords['minX']) 
					$area['x2'] = $area['minX'] = $smallWallCoords['minX'];	
				if ($area['x1']>$smallWallCoords['maxX'])
					$area['x1'] = $area['maxX'] = $smallWallCoords['maxX'];
				if ($area['x2']>$smallWallCoords['maxX'])
					$area['x2'] = $area['maxX'] = $smallWallCoords['maxX'];
				if ($area['y1']<$smallWallCoords['minY'])
					$area['y1'] = $area['minY'] = $smallWallCoords['minY'];
				if ($area['y2']<$smallWallCoords['minY'])
					$area['y2'] = $area['minY'] = $smallWallCoords['minY'];
				if ($area['y1']>$smallWallCoords['maxY'])
					$area['y1'] = $area['maxY'] = $smallWallCoords['maxY'];
				if ($area['y2']>$smallWallCoords['maxY'])
					$area['y2'] = $area['maxY'] = $smallWallCoords['maxY'];	
				return $area;
			}
		}
}

/**
 * Draws the coordinates onto the image
 * 
 * @param  $filename name of the gif image file
 * @param  $data     the data which was calculated
 * @param  $largeMap if the coordinates should be shown on the full map
 * @param  $link     draw Coords for the data where this specific link is given
 * @return 
 */
function drawCoords($filename, $data, $largeMap = false, $link = false)
{
	$im = imagecreatefromgif($filename);
	$black = ImageColorAllocate ($im, 0, 0, 0);
	foreach ($data as $room) {
		foreach ($room as $d) {
			if ($largeMap) {
				if (($d['link'] == $link) || ($link == false)) {
					$coordX = $d['coord-x'];
					$coordY = $d['coord-y'];
					$extentWidth = $d['extent-width'];
					$angleOfView = $d['angleOfView'];
					
					if ($angleOfView == '0' || $angleOfView == '180') {
						$x1 = $coordX - $extentWidth;
						$x2 = $coordX + $extentWidth;
						$y1 = $coordY;
						$y2 = $coordY;
					}
					if ($angleOfView == '90' || $angleOfView == '270') {
						$x1 = $coordX;
						$x2 = $coordX;
						$y1 = $coordY - $extentWidth;
						$y2 = $coordY + $extentWidth;
					}
					imagesetthickness($im, 5 );
					imageline($im, $x1 , $y1 , $x2 , $y2,0xFFFFFF);
				}
			}
			else 
			{
				$polygonCoords = defineCoords($d['polygon']);
				imagesetthickness($im, 5 );
				imagestring($im, 1, $polygonCoords['x1']+3, $polygonCoords['y1'], $d['angleOfView'], $black);
				imagestring($im, 1, $polygonCoords['x1']+3, $polygonCoords['y1']+10, $d['height-percent'], $black);
			}
		}
	}

	header("Content-type: image/gif");
	imagegif($im);
	imagedestroy($im);
}

/**
 * Searches for rectangles in gif files with specific indexed colors
 * 
 * @param  $fileName gif file
 * @param  $colors   array with colors to search for
 * @param  $border   amount of pixels wich are added to the found rectangles
 * @param  $cut      array with coordinates where the search starts or ends (x1,y1,x2,y2)
 * @return the areas with the specific color(s)
 */
function findAreasFromImage($fileName, $colors = array(2), $border=0, $cut = false)
{
	$im = imagecreatefromgif($fileName);
	$width = imagesx($im); // image width
	$height = imagesy($im); // image height
	// set starting coordinate default
	$startx = 0; 
	$starty = 0;
	if (isset($cut)) {
		if (array_key_exists('x1',$cut))
			$startx = $cut['x1'];
		if (array_key_exists('y1',$cut))
			$starty = $cut['y1'];
		if (array_key_exists('x2',$cut))
			$width = $cut['x2'];
		if (array_key_exists('y2',$cut))
			$height = $cut['y2'];
	}
	$i = 0;
	$firstLoop = true;
	$wasDetected = false;

	// process the image line for line
	foreach ($colors as $color) {
		for($y = $starty; $y < $height; $y++) {
			for($x = $startx; $x < $width; $x++) {
				// check if pixel has the correct color
				if (imagecolorat($im,$x,$y)==$color) {
					//stdOut("Color $color found at x:$x, y:$y");
					if (!$firstLoop) {
						//check if area is already detected
						foreach ($areas as $area) {
							if (($x>=$area['x1']) && 
								($x<=$area['x2']) &&
								($y>=$area['y1']) &&
								($y<=$area['y2']) &&
								($color==$area['color'])) {
								$wasDetected = true;
								break;
							} else {
								$wasDetected = false;
							}
						}
					}

					$tempX = $x;
					$tempY = $y;
					// define first coordinate 
					if (!$wasDetected) {
						// stdOut("Creating new area with starting coordinates $tempX and $tempY with index $i");
						$areas[$i]['x1'] = $tempX - $border;
						$areas[$i]['y1'] = $tempY - $border;
					}
					// find last correct color of area
					while (imagecolorat($im,$tempX,$tempY)==$color) {
						$tempX++;
					}
					$tempX--;
					if (!$wasDetected) {
						// stdOut("Last x coordinate for area with index $i is at $tempX");
						$areas[$i]['x2'] = $tempX + $border;

					}

					while (imagecolorat($im,$tempX,$tempY)==$color) {
						$tempY++;
					}
					if (!$wasDetected) {
						$areas[$i]['y2'] = $tempY + $border;
						$areas[$i]['color'] = $color;
						// stdOut("Last y coordinate for area with index $i is at $tempY");
					}
					
					$x = $tempX+1;
					$firstLoop = false;
					if (!$wasDetected) {
						$i++;
					}
				}
			}
		}
	}
	imagedestroy($im);
	return $areas;
}

/**
 * Checks for image maps
 * 
 * @param  $site URL of site
 * @return the found imagemaps
 */
function checkForImageMaps($site) {
	// Find all imagemaps on actual html site
    if ($maps = $site->find('map')) 
    	return $maps;
    else 
    	return false;
}

/**
 * Checks for image map areas
 * 
 * @param  $site 	URL of site
 * @return the found imagemaps areas
 */
function checkForAreas($site) {
    if ($areas = $site->find('area')) 
    	return $areas;
    else
    	return false;
}

/**
 * Calculates the non direct readable Informations for one area
 * Can be run with transformation toggle to reallign the coordinate system to the main coordinate system
 * 
 * @param  $areaString      	area coordinates string
 * @param  $link 				the link of the area      
 * @param  $wallAreaString  	the wall of the area, necessary for determine the height of the actual area
 * @param  $innerAreaString 	the "floor" of the given site/room
 * @param  $mainAreaString  	the "floor" of the given site/room on the main plan of the temple, necessary for transformation
 * @param  $angleOfViewList 	an array with angles which cannot be determined automatically
 * @param  $setting an array 	with angles which cannot be determined automatically
 * @param  $transform       	defines if the area is calculated to match the main plan of the temple
 * @return $data 				the relevant informations, which are calculated
 */
function calculate($areaString,$link,$wallAreaString,$innerAreaString,$mainAreaString,$angleOfViewList,$setting,$transform=false) {
	$area = defineCoords($areaString);
	if (!$area) {
		createRectangleFromPolygon($areaString);
		$area = defineCoords($areaString);
	}
	if ($wallAreaString)
		$wall = defineCoords($wallAreaString);
	$innerArea = defineCoords($innerAreaString);

	$middleX = $area['minX'] + ($area['maxX'] - $area['minX']) / 2;
	$middleY = $area['minY'] + ($area['maxY'] - $area['minY']) / 2;

	// on top of the innerArea, so set angle to north
	if (($middleY < $innerArea['minY'] && $setting=='inner') 
		|| ($middleY > $innerArea['maxY'] && $setting=='outer')) 
		$data['angleOfView'] = 0;
	
	// on the right of the inner Area or set manually, so set angle to east
	if (($middleX > $innerArea['maxX'] && $setting=='inner')
		|| ($middleX < $innerArea['minX'] && $setting=='outer')
		|| in_array($link, $angleOfViewList['90degrees'])
		|| in_array($areaString, $angleOfViewList['90degrees']))
		$data['angleOfView'] = 90;

	// further downwards than the inner Area, so set angle to south
	if (($middleY > $innerArea['maxY'] && $setting=='inner') 
		|| ($middleY < $innerArea['minY'] && $setting=='outer'))
		$data['angleOfView'] = 180;

	// on the left of the inner Area or set manually, so set angle to west
	if (($middleX < $innerArea['minX']  && $setting=='inner')
		|| ($middleX > $innerArea['maxX'] && $setting=='outer')
		|| in_array($link, $angleOfViewList['270degrees'])
		|| in_array($areaString, $angleOfViewList['270degrees']))
		$data['angleOfView'] = 270;

	$extent = array('x' => (($area['maxX'] - $area['minX']) / 2),
					'y' => (($area['maxY'] - $area['minY']) / 2));

	if ($transform)
		$extent = transformExtent($mainAreaString, $innerAreaString, $extent);

	if ($data['angleOfView'] == 0) {
		$data['coord-x'] = $middleX;
		if ($setting == 'inner')
			$data['coord-y'] = $wall['maxY'];
		if ($setting == 'outer')
			$data['coord-y'] = $wall['minY'];	
		$data['height-percent'] = round(($wall['maxY'] - $middleY) / ($wall['maxY'] - $wall['minY']) * 100, NUMBERTAIL);;	
		$data['extent-width'] = $extent['x'];
		$data['extent-height-percent'] = round((($area['maxY'] - $area['minY']) / ($wall['maxY'] - $wall['minY'])) * 100 / 2, NUMBERTAIL);
	}

	if ($data['angleOfView'] == 180) {
		$data['coord-x'] = $middleX;
		if ($setting == 'inner')
			$data['coord-y'] = $wall['minY'];
		if ($setting == 'outer')
			$data['coord-y'] = $wall['maxY'];	
		$data['height-percent'] = round(($middleY - $wall['minY']) / ($wall['maxY'] - $wall['minY']) * 100, NUMBERTAIL);
		$data['extent-width'] = $extent['x'];
		$data['extent-height-percent'] = round((($area['maxY'] - $area['minY']) / ($wall['maxY'] - $wall['minY'])) * 100 / 2, NUMBERTAIL);
	}

	if ($data['angleOfView'] == 90) {
		if ($wallAreaString) {
			if ($setting == 'inner')
				$data['coord-x'] = $wall['minX'];
			if ($setting == 'outer')
				$data['coord-x'] = $wall['maxX'];
			$data['coord-y'] = $middleY;
			$data['height-percent'] = round(($middleX - $wall['minX']) / ($wall['maxX'] - $wall['minX']) * 100, NUMBERTAIL);	
			$data['extent-width'] = $extent['y'];
			$data['extent-height-percent'] = round(($area['maxX'] - $area['minX']) / ($wall['maxX'] - $wall['minX']) * 100 / 2, NUMBERTAIL);
		}
		// innerlying areas
		else {
			$data['coord-x'] = $area['minX'];
			$data['coord-y'] = $middleY;
			// set innerlying areas to height-percent 50
			$data['height-percent'] = 50;
			$data['extent-width'] = $extent['y'];
			$data['extent-height-percent'] = 50;
		}
	}

	if ($data['angleOfView'] == 270) {
		if ($wallAreaString) {
			if ($setting == 'inner')
				$data['coord-x'] = $wall['maxX'];
			if ($setting == 'outer')
				$data['coord-x'] = $wall['minX'];
			$data['coord-y'] = $middleY;
			$data['height-percent'] = round(($wall['maxX'] - $middleX) / ($wall['maxX'] - $wall['minX']) * 100, NUMBERTAIL);	
			//$data['height-percent'] = round(($middleX - $wall['maxX']) / ($wall['minX'] - $wall['maxX']) * 100, NUMBERTAIL);	
			$data['extent-width'] = $extent['y'];
			$data['extent-height-percent'] = round(($area['maxX'] - $area['minX']) / ($wall['maxX'] - $wall['minX']) * 100 / 2, NUMBERTAIL);
		} 
		// innerlying areas
		else {
			$data['coord-x'] = $area['maxX'];
			$data['coord-y'] = $middleY;
			// set innerlying areas to height-percent 50
			$data['height-percent'] = 50;
			$data['extent-width'] = $extent['y'];
			$data['extent-height-percent'] = 50;
		}
	}

	if ($transform) {
		$newCoord = transformCoords($mainAreaString, $innerAreaString, $data['coord-x'], $data['coord-y']);
		$data['coord-x'] = $newCoord['x'];
		$data['coord-y'] = $newCoord['y'];
		$data['coord-y'] = $data['coord-y'];
	}
	return $data;
}

/**
 * Transforms one coordinate into the main temple plan
 * 
 * @param  $mainAreaString coordinates of the given area (e.g. court) on main temple plan
 * @param  $newAreaString  coordinates of the floor plan of the given area (eg. court)
 * @param  $coordX         x value of coordinate that should be transformed
 * @param  $coordY         y value of coordinate that should be transformed
 * @return the transformed coordinates
 */
function transformCoords($mainAreaString, $newAreaString, $coordX, $coordY)
{
	$mainArea = defineCoords($mainAreaString);
	$newArea = defineCoords($newAreaString);
	$scale = checkScaleRatio($mainArea, $newArea);

	$newCoordX = round($mainArea['minX'] + (($coordX - $newArea['minX']) * $scale['x']),NUMBERTAIL);
	$newCoordY = round($mainArea['minY'] + (($coordY - $newArea['minY']) * $scale['y']),NUMBERTAIL);
	return $ret = array('x' => $newCoordX, 
						'y' => $newCoordY);
}

/**
 * Transforms the extent value 
 * 
 * @param  $mainAreaString coordinates of the given area (e.g. court) on main temple plan
 * @param  $newAreaString  coordinates of the floor plan of the given area (eg. court)
 * @param  $extent         values(x and y) of the extent that should be transformed
 * @return the transformed extent
 */
function transformExtent($mainAreaString, $newAreaString, $extent) {
	$mainArea = defineCoords($mainAreaString);
	$newArea = defineCoords($newAreaString);
	$scale = checkScaleRatio($mainArea, $newArea);
	$extent['x']= round($extent['x'] * $scale['x'],NUMBERTAIL);
	$extent['y']= round($extent['y'] * $scale['y'],NUMBERTAIL);
	return $extent;
}

/**
 * Looks up on which wall the area lies
 * 
 * @param  $wallAreas  array with all wall coordinates
 * @param  $areaString area
 * @return the correct wall
 */
function checkPosition($wallAreas, $areaString)
{
	$area = defineCoords($areaString);
	$i = 0;
	foreach ($wallAreas as $wall) {
		$wallCoords = defineCoords($wall);	
		if (($area['maxX']-3<=$wallCoords['maxX']) &&
			($area['minX']+3>=$wallCoords['minX']) &&
			($area['maxY']-3<=$wallCoords['maxY']) &&
			($area['minY']+3>=$wallCoords['minY'])) {
				return $wall;
		}
	}
	return $wall = false;
}

/**
 * calculates scale ratio
 * 
 * @param  $mainArea coordinates of the given area (e.g. court) on main temple plan
 * @param  $newArea  coordinates of the floor plan of the given area (eg. court)
 * @return the scale ratio 	 
 */
function checkScaleRatio($mainArea, $newArea) {
	$scale['x'] = ($mainArea['maxX'] - $mainArea['minX'])
		/  ($newArea['maxX'] - $newArea['minX']);
	$scale['y'] = ($mainArea['maxY'] - $mainArea['minY']) 
		/  ($newArea['maxY'] - $newArea['minY']);
	return $scale;
}

/**
 * rotates a coordinate depending on the angle and the center of rotation
 * 
 * @param  $x 		the x coordinate
 * @param  $y 		the y coordinate
 * @param  $center 	the rotation center
 * @param  $angle 	the angle
 * @return array with rotated x- any y-value of coordinate
 */
function rotatePoint($x, $y, $center, $angle)
{
	$newX = $center['x'] + ($x - $center['x']) * cos($angle) - ($y - $center['y']) * sin($angle);
	$newY = $center['y'] + ($x - $center['x']) * sin($angle) + ($y - $center['y']) * cos($angle);
	return $ret = array('x'=>$newX,'y'=> $newY);
}

/**
 * calculates the angle of a line (hypotenuse) in reference to the y-axis
 * @param  $hypotenuse the hypotenuse/ the side which is used to calculate the angle to axis
 * @return the calculated angle
 */
function calculateAngle($hypotenuse)
{
	$hypotenuse = defineCoords($hypotenuse);
	$adjacentLeg = $hypotenuse['maxX'] - $hypotenuse['minX'];
	$oppositeLeg = $hypotenuse['maxY'] - $hypotenuse['minY'];
	return $angle = atan($adjacentLeg/$oppositeLeg);
}

/**
 * changes coordinate from left hand coordinate system (y down) to right hand (y up)
 * 
 * @param  $x 		x-value of coordinate
 * @param  $y 		y-value of coordinate
 * @param  $maxY 	the biggest possible y-coordinate in the system (e.g. in an image the y-size of the image)
 * 
 * @return $newCoords	
 */
function moveToRightHandSystem($x,$y,$maxY)
{
	$newY = -1*($y-$maxY);
	return array('x' => $x,'y' => $newY);
}

/**
 * rotates a rectangle to the axis
 *
 * @param  $hypotenuse the hypotenuse/ the side which is used to calculate the angle to axis
 * @param  $center 	   the rotation point
 * @param  $coords     the rectangle coordinates
 * @return the rotated coordinates
 */
function rotateToAxis($hypotenuse,$center,$coords)
{
	$angle = calculateAngle($hypotenuse);
	$rotatedCoords = array();
	foreach ($coords as $coord) {
		$rotatedCoords[] = rotatePoint($coord['x'],$coord['y'],$center,$angle);
	}
	return $rotatedCoords;
}
?>