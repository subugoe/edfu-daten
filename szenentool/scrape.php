<?php
require_once(dirname(__FILE__).'/lib/functions.php');
require_once(dirname(__FILE__).'/config.php');

foreach ($rooms as $room) {
	if (isset($room['cut']))
		$cut = $room['cut'];
	else 
		$cut = false;
	$data = run($room,$lists);
	createCsv($data, $room['fileName']);
}

// draw coords on temple plan
$fileName = 'file:///P:/ENT/edfu/site_offline/Plans/tempel_right.gif';
// @drawCoords($fileName, $data, true);


// draw coords on room plan
// foreach ($rooms as $room) {
// 		@drawCoords($room['url'], $data);
// }

// temporary for gathering wall coordinates
// $missingCoords = array(25,400,375,40); //y from northwall, x from eastwall, y from southwall, x from westwall
// $wallcoords = giveWallCoords('169,140,284,241',$missingCoords);
// print_r($wallcoords);

?>