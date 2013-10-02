<?php

mb_internal_encoding("UTF-8");
// Number of decimal places
const NUMBERTAIL = 2;

$url = 'data/';

$rooms = array(	
				'pylon' => array(
					'mainArea' => '56,715,431,775', // area of this room on main temple plan
					'area' => '189,265,503,305', // area of this room on detailed room view (floor without walls)
					'walls' => array( // the wall-coordinates
						'149,305,547,485',
						'114,85,547,265',
						'503,244,674,326',
						'17,243,189,328'
						),
					'url' => $url . 'Pylon.html', // url to the document
					'fileName' => 'pylon.csv', // target
					'setting' => 'outer', // 'inner' or 'outer', describes the perspective
					'cut' => array( // the image can be cut, e.g x1 marks the starting x-coordinate, y2 the ending y-coordinate
						'y2' => '495'
						)
					),
				// 'pylon_white' => array(
				// 	'mainArea' => '56,715,431,775',
				// 	'area' => '189,265,503,305',
				// 	'walls' => array(
				// 		'149,305,547,485',
				// 		'114,85,547,265',
				// 		'503,244,674,326',
				// 		'17,243,189,328'
				// 		),						
				// 	'url' => $url . 'pylon_3.gif',
				// 	'fileName' => 'pylon_white.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'y2' => '492'
				// 		),
				// 	'onlyWhite' => true // if only white areas shoud be searched for set to true
				// 	),
				// 	
				// 'pylon_door' => array(
				// 	'mainArea' => '229,715,258,774',
				// 	'area' => '130,60,240,182',
				// 	'walls' => array(
				// 		'35,60,131,182',
				// 		'240,60,335,182',
				// 		),
				// 	'url' => $url . 'Pylon_door.html',
				// 	'fileName' => 'pylon_door.csv',
				// 	'setting' => 'inner',
				// 	),
				// 	
				// 'pylon_door_white' => array(
				// 	'mainArea' => '229,715,258,774',
				// 	'area' => '130,60,240,182',
				// 	'walls' => array(
				// 		'35,73,131,169',
				// 		'239,73,335,169',
				// 		),
				// 	'url' => $url . 'pylon_door_edited_2.gif',
				// 	'fileName' => 'pylon_tuerlaibungen_white.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(
				// 		),
				// 	'onlyWhite' => true
				// 	),
				// 	
				// 'pylon_upper_part' => array(
				// 'mainArea' => '200,716,287,775',
				// 'area' => '333,264,358,305',
				// 'walls' => array(
				// 	'321,264,334,305',
				// 	'357,264,370,305',
				// 	),
				// 'url' => $url . 'pylon_6.gif',
				// 'fileName' => 'pylon_upperpart_white.csv',
				// 'setting' => 'inner',
				// 'cut' => array(
				// 	'x1' => 321,
				// 	'y1' => 263,
				// 	'x2' => 370,
				// 	'y2' => 305
				// 	),
				// 	'onlyWhite' => true
				// ),
				// 	
				// 'court' => array(
				// 	'mainArea' => '123,459,361,716',
				// 	'area' => '130,40,480,470',
				// 	'walls' => array(
				// 		'49,40,130,470',
				// 		'129,470,480,550',
				// 		'480,40,560,470'
				// 		),
				// 	'url' => $url . 'Hof.html',
				// 	'fileName' => 'court.csv',
				// 	'setting' => 'inner',
				// 	),
				// 'court_white' => array(
				// 	'mainArea' => '123,459,361,716',
				// 	'area' => '130,40,480,470',
				// 	'walls' => array(
				// 		'49,40,130,470',
				// 		'129,470,480,550',
				// 		'480,40,560,470'
				// 		),
				// 	'url' => $url . 'court_2.gif',
				// 	'fileName' => 'court_white.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(
						
				// 		),
				// 	'onlyWhite' => true
				// 	),
				// 	
				// 'wall' => array(
				// 	'mainArea' => '114,11,371,720',
				// 	'area' => '121,166,360,1386',
				// 	'walls' => array(
				// 		'41,164,121,1386',
				// 		'119,88,362,166',
				// 		'360,164,438,1386'
				// 		),
				// 	'url' => $url . 'Wall.html',
				// 	'fileName' => 'wall.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(),
				// 	),
				// 'wall_white' => array(
				// 	'mainArea' => '114,11,371,720',
				// 	'area' => '121,166,360,1386',
				// 	'walls' => array(
				// 		'41,164,121,1386',
				// 		'119,88,362,166',
				// 		'360,164,438,1386'
				// 		),
				// 	'url' => $url . 'wall_2.gif',
				// 	'fileName' => 'wall_white.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		),
				// 	'onlyWhite' => true,
				// 	),
				// 	
				// 'innerwall' => array(
				// 	'mainArea' => '123,22,361,460',
				// 	'area' => '136,187,403,1099',
				// 	'walls' => array(
				// 		'23,185,136,1099',
				// 		'403,185,516,1099',
				// 		'134,74,405,187'
				// 		),
				// 	'url' => $url . 'Innerwall.html',
				// 	'fileName' => 'innerwall.csv',
				// 	'setting' => 'inner',
				// 	),
				// 	
				// 'innerwall_white' => array(
				// 	'mainArea' => '122,21,362,460',
				// 	'area' => '136,187,403,1099',
				// 	'walls' => array(
				// 		'23,185,136,1099',
				// 		'403,185,516,1099',
				// 		'134,74,405,187'
				// 		),
				// 	'url' => $url . 'innerwall.gif',
				// 	'fileName' => 'innerwall_white.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(),
				// 	'onlyWhite' => true
				// 	),
				// 	
				// 'Raum_A' => array(
				// 	'mainArea' => '228,122,260,183',
				// 	'area' => '155,134,250,324',
				// 	'walls' => array(
				// 		'152,22,252,134',
				// 		'251,132,370,326',
				// 		'152,324,252,440',
				// 		'34,132,155,326'
				// 		),
				// 	'url' => $url . 'Raum_A.gif',
				// 	'fileName' => 'Raum_A.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(
				// 		'y2' => '443')
				// 	),
				// 'Raum_A_aussentuer' => array(
				// 	'mainArea' => '221,180,268,192',
				// 	'area' => '122,439,281,450',
				// 	'walls' => array(
				// 		'122,450,281,554',
				// 		),
				// 	'url' => $url . 'Raum_A.gif',
				// 	'fileName' => 'Raum_A_2.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'y1' => '443',
				// 		),
				// 	),
				// 	
				// 'Raum_As' => array(
				// 	'mainArea' => '167,306,181,348',
				// 	'area' => '261,139,320,314',
				// 	'walls' => array(
				// 		'260,26,321,139',
				// 		'319,139,441,314',
				// 		'260,314,321,437',
				// 		'141,139,261,314',
				// 		),
				// 	'url' => $url . 'Raum_As.gif',
				// 	'fileName' => 'Raum_As.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(
				// 		'x1' => '136')
				// 	),
				// 'Raum_As_aussentuer' => array(
				// 	'mainArea' => '164,307,168,316',
				// 	'area' => '127,135,142,205',
				// 	'walls' => array(
				// 		'32,132,128,206',
				// 		'127,58,143,136'
				// 		),
				// 	'url' => $url . 'Raum_As_2.gif',
				// 	'fileName' => 'Raum_As_aussentuer.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'x2' => '142',
				// 		),
				// 	),
					
				// 'Raum_B' => array(
				// 	'mainArea' => '306,308,319,348',
				// 	'area' => '143,219,181,398',
				// 	'walls' => array(
				// 		'143,100,181,220',
				// 		'180,219,301,398',
				// 		'143,397,181,517',
				// 		'23,219,144,398'
				// 		),
				// 	'url' => $url . 'Raum_B.gif',
				// 	'fileName' => 'Raum_B.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(
				// 		'y1' => '102'
				// 		),
				// 	),
				// 'Raum_B_aussentuer' => array(
				// 	'mainArea' => '307,305,314,313',
				// 	'area' => '138,90,182,101',
				// 	'walls' => array(
				// 		'139,15,182,92',
				// 		'181,90,241,102'
				// 		),
				// 	'url' => $url . 'Raum_B_2.gif',
				// 	'fileName' => 'Raum_B_aussentuer.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'y2' => '102',
				// 		),
				// 	),
					
				// 'Raum_C' => array(
				// 	'mainArea' => '146,365,339,443',
				// 	'area' => '183,142,499,285',
				// 	'walls' => array(
				// 		'183,24,499,143',
				// 		'498,142,619,285',
				// 		'183,284,499,402',
				// 		'63,142,184,285'
				// 		),
				// 	'url' => $url . 'Raum_C_4.gif',
				// 	'fileName' => 'Raum_C.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(
				// 		'y2' => '408',
				// 		'x2' => '630'
				// 		),
				// 	),
				// 'Raum_C_aussentuer_rechts' => array(
				// 	'mainArea' => '339,389,345,399',
				// 	'area' => '632,180,639,223',
				// 	'walls' => array(
				// 		'632,208,638,249',
				// 		'638,180,714,223',
				// 		),
				// 	'url' => $url . 'Raum_C_5.gif',
				// 	'fileName' => 'Raum_C_aussentuer_rechts.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'x1' => '618',
				// 		),
				// 	),
				// 'Raum_C_aussentuer_unten' => array(
				// 	'mainArea' => '131,442,353,449',
				// 	'area' => '178,401,507,513',
				// 	'walls' => array(
				// 		'180,512,506,615',
				// 		),
				// 	'url' => $url . 'Raum_C_5.gif',
				// 	'fileName' => 'Raum_C_aussentuer_unten.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'y1' => '450',
				// 		'y2' => '618',
				// 		'x1' => '170',
				// 		'x2' => '523'
				// 		),
				// 	),

				// 'Raum_C_tuerlaibung_tor' => array(
				// 	'mainArea' => '227,432,258,451',
				// 	'area' => '326,459,360,511',
				// 	'walls' => array(
				// 		'359,459,462,511',
				// 		'224,460,327,512'
				// 		),
				// 	'url' => $url . 'Raum_C_6.gif',
				// 	'fileName' => 'Raum_C_tuerlaibung_unten.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'y1' => '452',
				// 		'y2' => '512',
				// 		'x1' => '222',
				// 		'x2' => '462'
				// 		),
				// 	),
				// 	
				// 'Raum_C_laibung_untenrechts' => array(
				// 	'mainArea' => '320,438,332,452',
				// 	'area' => '463,489,482,514',
				// 	'walls' => array(
				// 		'481,489,583,513',
				// 		),
				// 	'url' => $url . 'Raum_C_7.gif',
				// 	'fileName' => 'Raum_C_tuerlaibung_untenrechts.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'y1' => '485',
				// 		'y2' => '514',
				// 		'x1' => '463',
				// 		),
				// 	),

				// 'Raum_C_laibung_untenlinks' => array(
				// 	'mainArea' => '151,438,167,451',
				// 	'area' => '203,489,223,513',
				// 	'walls' => array(
				// 		'102,489,203,513',
				// 		),
				// 	'url' => $url . 'Raum_C_7.gif',
				// 	'fileName' => 'Raum_C_tuerlaibung_untenlinks.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'y1' => '485',
				// 		'y2' => '514',
				// 		'x2' => '222',
				// 		),
				// 	),
				// 	
				// 'Raum_C_architrave' => array(
				// 	'mainArea' => '146,365,339,443',
				// 	'area' => '183,142,499,285',
				// 	'walls' => array(
				// 		'183,24,499,143',
				// 		'498,142,619,285',
				// 		'183,284,499,402',
				// 		'63,142,184,285'
				// 		),
				// 	'url' => $url . 'Raum_C_architrave_2.gif',
				// 	'fileName' => 'Raum_C_architrave.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(
				// 		'y2' => '408',
				// 		'x2' => '630'
				// 		),
				// 	),

				// 'Raum_D' => array(
				// 	'mainArea' => '174,161,201,186',
				// 	'area' => '135,125,251,205',
				// 	'walls' => array(
				// 		'135,7,251,125',
				// 		'250,125,368,205',
				// 		'135,204,251,323',
				// 		'16,125,136,205'
				// 		),
				// 	'url' => $url . 'Raum_D.gif',
				// 	'fileName' => 'Raum_D.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(
				// 		'x2' => '373'
				// 		)
				// 	),
				// 'Raum_D_aussentuer' => array(
				// 	'mainArea' => '200,166,210,176',
				// 	'area' => '367,125,379,205',
				// 	'walls' => array(
				// 		'378,125,484,205',
				// 		),
				// 	'url' => $url . 'Raum_D.gif',
				// 	'fileName' => 'Raum_D_aussentuer.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'x1' => '373',
				// 		),
				// 	),
				// 	
				// 'Raum_E' => array(
				// 	'mainArea' => '174,131,200,155',
				// 	'area' => '134,134,250,214',
				// 	'walls' => array(
				// 		'134,16,250,135',
				// 		'249,134,368,214',
				// 		'134,213,250,332',
				// 		'15,134,135,214'
				// 		),
				// 	'url' => $url . 'Raum_E.gif',
				// 	'fileName' => 'Raum_E.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(
				// 		'x2' => '373'
				// 		)
				// 	),
				// 'Raum_E_aussentuer' => array(
				// 	'mainArea' => '199,130,207,156',
				// 	'area' => '367,134,378,214',
				// 	'walls' => array(
				// 		'378,134,484,214',
				// 		),
				// 	'url' => $url . 'Raum_E.gif',
				// 	'fileName' => 'Raum_E_aussentuer.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'x1' => '373',
				// 		),
				// 	),
					
				// 'Raum_F' => array(
				// 	'mainArea' => '173,98,200,124',
				// 	'area' => '131,134,247,214',
				// 	'walls' => array(
				// 		'131,16,247,135',
				// 		'246,134,366,214',
				// 		'131,213,247,332',
				// 		'12,134,132,214'
				// 		),
				// 	'url' => $url . 'Raum_F.gif',
				// 	'fileName' => 'Raum_F.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(
				// 		'x2' => '370'
				// 		)
				// 	),
				// 'Raum_F_aussentuer' => array(
				// 	'mainArea' => '199,98,209,124',
				// 	'area' => '365,134,375,214',
				// 	'walls' => array(
				// 		'374,134,482,214'
				// 		),
				// 	'url' => $url . 'Raum_F.gif',
				// 	'fileName' => 'Raum_F_aussentuer.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'x1' => '370',
				// 		),
				// 	),
				// 	
				// 'Raum_G' => array(
				// 	'mainArea' => '200,71,225,93',
				// 	'area' => '169,140,284,241',
				// 	'walls' => array(
				// 		'169,25,284,140',
				// 		'283,140,401,241',
				// 		'169,240,284,376',
				// 		'40,140,170,241'
				// 		),
				// 	'url' => $url . 'Raum_G_2.gif',
				// 	'fileName' => 'Raum_G.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(
				// 		'y2' => '390'
				// 		)
				// 	),
				// 'Raum_G_aussentuer' => array(
				// 	'mainArea' => '207,91,226,102',
				// 	'area' => '176,375,276,404',
				// 	'walls' => array(
				// 		'176,403,276,530'
				// 		),
				// 	'url' => $url . 'Raum_G_2.gif',
				// 	'fileName' => 'Raum_G_aussentuer.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'y1' => '390',
				// 		),
				// 	),
					
				// 'Raum_H' => array(
				// 	'mainArea' => '173,71,195,93',
				// 	'area' => '172,136,287,216',
				// 	'walls' => array(
				// 		'170,18,289,137',
				// 		'286,134,405,218',
				// 		'170,215,289,332',
				// 		'54,134,173,218'
				// 		),
				// 	'url' => $url . 'Raum_H_3.gif',
				// 	'fileName' => 'Raum_H.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(
				// 		),
				// 	),
				// 	
				// 'Raum_I' => array(
				// 	'mainArea' => '230,71,257,93',
				// 	'area' => '167,134,247,197',
				// 	'walls' => array(
				// 		'167,15,247,134',
				// 		'247,134,364,197',
				// 		'167,197,247,314',
				// 		'49,134,167,197'
				// 		),
				// 	'url' => $url . 'Raum_I.gif',
				// 	'fileName' => 'Raum_I.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(
				// 		'y2' => '319'
				// 		)
				// 	),
				// 'Raum_I_aussentuer' => array(
				// 	'mainArea' => '231,92,256,102',
				// 	'area' => '165,314,249,325',
				// 	'walls' => array(
				// 		'166,324,249,430'
				// 		),
				// 	'url' => $url . 'Raum_I.gif',
				// 	'fileName' => 'Raum_I_aussentuer.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'y1' => '319',
				// 		),
				// 	),
				// 	
				// 'Raum_J' => array(
				// 	'mainArea' => '262,71,287,93',
				// 	'area' => '173,125,288,240',
				// 	'walls' => array(
				// 		'173,9,288,125',
				// 		'288,125,417,240',
				// 		'173,240,288,368',
				// 		'55,125,173,240',
				// 		),
				// 	'url' => $url . 'Raum_J.gif',
				// 	'fileName' => 'Raum_J.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(
				// 		'y2' => '380'
				// 		)
				// 	),
				// 'Raum_J_aussentuer' => array(
				// 	'mainArea' => '263,92,280,102',
				// 	'area' => '171,368,290,396',
				// 	'walls' => array(
				// 		'179,396,283,524'
				// 		),
				// 	'url' => $url . 'Raum_J.gif',
				// 	'fileName' => 'Raum_J_aussentuer.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'y1' => '380',
				// 		),
				// 	),
				// 	
				// 'Raum_K' => array(
				// 	'mainArea' => '293,71,313,93',
				// 	'area' => '268,133,383,213',
				// 	'walls' => array(
				// 		'268,16,383,133',
				// 		'383,133,501,213',
				// 		'268,213,383,330',
				// 		'149,133,268,213',
				// 		),
				// 	'url' => $url . 'Raum_K.gif',
				// 	'fileName' => 'Raum_K.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(
				// 		'x1' => '141'
				// 		)
				// 	),
				// 'Raum_K_aussentuer' => array(
				// 	'mainArea' => '286,71,293,93',
				// 	'area' => '135,134,150,213',
				// 	'walls' => array(
				// 		'35,132,136,215'
				// 		),
				// 	'url' => $url . 'Raum_K.gif',
				// 	'fileName' => 'Raum_K_aussentuer.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'x2' => '141',
				// 		),
				// 	),
				// 	
				// 'Raum_L' => array(
				// 	'mainArea' => '286,98,313,125',
				// 	'area' => '252,140,367,220',
				// 	'walls' => array(
				// 		'252,23,367,140',
				// 		'367,140,485,220',
				// 		'252,220,367,337',
				// 		'133,139,253,220',
				// 		),
				// 	'url' => $url . 'Raum_L.gif',
				// 	'fileName' => 'Raum_L.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(
				// 		'x1' => '126'
				// 		)
				// 	),
				// 'Raum_L_aussentuer' => array(
				// 	'mainArea' => '277,98,287,125',
				// 	'area' => '117,141,134,219',
				// 	'walls' => array(
				// 		'18,138,118,221'
				// 		),
				// 	'url' => $url . 'Raum_L.gif',
				// 	'fileName' => 'Raum_L_aussentuer.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'x2' => '126',
				// 		),
				// 	),
					
				// 'Raum_M' => array(
				// 	'mainArea' => '286,131,313,158',
				// 	'area' => '252,140,367,220',
				// 	'walls' => array(
				// 		'252,23,367,140',
				// 		'367,140,485,220',
				// 		'252,220,367,337',
				// 		'133,140,253,220',
				// 		),
				// 	'url' => $url . 'Raum_M.gif',
				// 	'fileName' => 'Raum_M.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(
				// 		'x1' => '126'
				// 		)
				// 	),
				// 'Raum_M_aussentuer' => array(
				// 	'mainArea' => '277,131,286,158',
				// 	'area' => '117,141,134,219',
				// 	'walls' => array(
				// 		'18,139,118,220'
				// 		),
				// 	'url' => $url . 'Raum_M.gif',
				// 	'fileName' => 'Raum_M_aussentuer.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'x2' => '126',
				// 		),
				// 	),
					

				// 'Raum_N' => array(
				// 	'mainArea' => '208,190,278,219',
				// 	'area' => '176,177,415,275',
				// 	'walls' => array(
				// 		'176,28,415,177',
				// 		'415,177,556,275',
				// 		'176,275,415,427',
				// 		'31,177,176,275'
				// 		),
				// 	'url' => $url . 'Raum_N_2.gif',
				// 	'fileName' => 'Raum_N.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(
				// 		'y2' => '449'
				// 		)
				// 	),
				// 'Raum_N_aussentuer' => array(
				// 	'mainArea' => '225,217,263,231',
				// 	'area' => '236,427,355,479',
				// 	'walls' => array(
				// 		'236,478,355,672'
				// 		),
				// 	'url' => $url . 'Raum_N_2.gif',
				// 	'fileName' => 'Raum_N_aussentuer.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'y1' => '449',
				// 		),
				// 	),
				// 	
				// 'Raum_O' => array(
				// 	'mainArea' => '174,191,201,219',
				// 	'area' => '144,129,259,209',
				// 	'walls' => array(
				// 		'144,11,259,129',
				// 		'259,129,377,209',
				// 		'144,209,259,325',
				// 		'25,129,144,209'
				// 		),
				// 	'url' => $url . 'Raum_O_2.gif',
				// 	'fileName' => 'Raum_O.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(
				// 		'x2' => '388'
				// 		)
				// 	),
				// 'Raum_O_aussentuer' => array(
				// 	'mainArea' => '200,192,209,218',
				// 	'area' => '377,130,398,209',
				// 	'walls' => array(
				// 		'397,130,493,209'
				// 		),
				// 	'url' => $url . 'Raum_O_2.gif',
				// 	'fileName' => 'Raum_O_aussentuer.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'x1' => '388',
				// 		),
				// 	),
				// 	
				// 'Raum_P' => array(
				// 	'mainArea' => '286,163,313,188',
				// 	'area' => '192,127,332,231',
				// 	'walls' => array(
				// 		'192,3,332,127',
				// 		'332,127,456,231',
				// 		'192,231,332,395',
				// 		'68,127,192,231',
				// 		),
				// 	'url' => $url . 'Raum_P_2.gif',
				// 	'fileName' => 'Raum_P.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(
				// 		'y2' => '408'
				// 		)
				// 	),
				// 'Raum_P_aussentuer' => array(
				// 	'mainArea' => '285,187,313,193',
				// 	'area' => '192,395,332,423',
				// 	'walls' => array(
				// 		'192,422,332,624'
				// 		),
				// 	'url' => $url . 'Raum_P_2.gif',
				// 	'fileName' => 'Raum_P_aussentuer.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'y1' => '408',
				// 		),
				// 	),
					
				// 'Raum_Q' => array(
				// 	'mainArea' => '286,192,313,219',
				// 	'area' => '258,117,375,234',
				// 	'walls' => array(
				// 		'259,115,373,116',
				// 		'375,116,460,235',
				// 		'258,234,375,319',
				// 		'157,116,259,235',
				// 		),
				// 	'url' => $url . 'Raum_Q_3.gif',
				// 	'fileName' => 'Raum_Q.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(
				// 		'x1' => '143'
				// 		)
				// 	),
				// 'Raum_Q_aussentuer' => array(
				// 	'mainArea' => '277,193,287,219',
				// 	'area' => '130,114,158,237',
				// 	'walls' => array(
				// 		'31,146,131,209'
				// 		),
				// 	'url' => $url . 'Raum_Q_3.gif',
				// 	'fileName' => 'Raum_Q_aussentuer.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'x2' => '143',
				// 		),
				// 	),
					
				// 'Raum_R' => array(
				// 	'mainArea' => '208,229,284,256',
				// 	'area' => '207,209,443,309',
				// 	'walls' => array(
				// 		'207,56,443,209',
				// 		'443,209,608,309',
				// 		'207,309,443,466',
				// 		'31,209,207,309',
				// 		),
				// 	'url' => $url . 'Raum_R_4.gif',
				// 	'fileName' => 'Raum_R.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(
				// 		'y2' => '465'
				// 		)
				// 	),
					
				// 'Raum_R_aussentuer' => array(
				// 	'mainArea' => '223,254,263,269',
				// 	'area' => '264,466,390,502',
				// 	'walls' => array(
				// 		'264,501,390,641',
				// 		'192,466,291,502',
				// 		'362,466,461,502'
				// 		),
				// 	'url' => $url . 'Raum_R_4.gif',
				// 	'fileName' => 'Raum_R_aussentuer.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'y1' => '465',
				// 		),
				// 	),
					
				// 'Raum_S' => array(
				// 	'mainArea' => '165,229,201,256',
				// 	'area' => '139,141,255,219',
				// 	'walls' => array(
				// 		'139,16,255,141',
				// 		'255,141,373,219',
				// 		'139,219,255,343',
				// 		'17,141,139,219'
				// 		),
				// 	'url' => $url . 'Raum_S_2.gif',
				// 	'fileName' => 'Raum_S.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(
				// 		'x2' => '372'
				// 		)
				// 	),
				// 'Raum_S_aussentuer' => array(
				// 	'mainArea' => '199,234,210,256',
				// 	'area' => '373,160,384,219',
				// 	'walls' => array(
				// 		'383,160,472,219',
				// 		'373,199,384,266'
				// 		),
				// 	'url' => $url . 'Raum_S_2.gif',
				// 	'fileName' => 'Raum_S_aussentuer.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'x1' => '372',
				// 		),
				// 	),
				
				// 'Raum_V' => array(
				// 	'mainArea' => '297,218,308,229',
				// 	'area' => '131,135,189,191',
				// 	'walls' => array(
				// 		'131,31,189,135',
				// 		'189,135,289,191',
				// 		'131,191,189,295',
				// 		'30,135,131,191'
				// 		),
				// 	'url' => $url . 'Raum_V_2.gif',
				// 	'fileName' => 'Raum_V.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(
				// 		'y2' => '293'
				// 		)
				// 	),
				// 'Raum_V_aussentuer' => array(
				// 	'mainArea' => '299,228,308,232',
				// 	'area' => '131,295,189,321',
				// 	'walls' => array(
				// 		'56,295,132,321',
				// 		'156,295,232,321'
				// 		),
				// 	'url' => $url . 'Raum_V_2.gif',
				// 	'fileName' => 'Raum_V_aussentuer.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(
				// 		'y1' => '293'
				// 		)
				// 	),
				// 	

				// 'Raum_W' => array(
				// 'mainArea' => '189,268,298,349',
				// 'area' => '176,188,437,426',
				// 'walls' => array(
				// 	'176,36,437,189',
				// 	'436,188,589,426',
				// 	'176,425,437,577',
				// 	'24,188,177,425'
				// 	),
				// 'url' => $url . 'Raum_W_2.gif',
				// 'fileName' => 'Raum_W.csv',
				// 'setting' => 'inner',
				// 'cut' => array(
				// 	'y2' => '576'
				// 	)
				// ),

				// 'Raum_W_aussentuer' => array(
				// 'mainArea' => '220,346,266,366',
				// 'area' => '262,576,354,594',
				// 'walls' => array(
				// 	'264,594,352,737',
				// 	'174,576,285,595'
				// 	),
				// 'url' => $url . 'Raum_W_3.gif',
				// 'fileName' => 'Raum_W_aussentuer.csv',
				// 'setting' => 'outer',
				// 'cut' => array(
				// 	'y1' => '576'
				// 	)
				// ),

				// 'Raum_W_tuerlaibungrechtsoben' => array(
				// 'mainArea' => '296,270,300,278',
				// 'area' => '480,185,489,229',
				// 'walls' => array(
				// 	'481,156,488,198',
				// 	),
				// 'url' => $url . 'Raum_W_tuerlaibungen.gif',
				// 'fileName' => 'Raum_W_tuerlaibungrechtsoben.csv',
				// 'setting' => 'outer',
				// 'cut' => array(
				// 	'x1' => '184'
				// 	)
				// ),
				// 'Raum_W_tuerlaibunglinksunten' => array(
				// 'mainArea' => '179,311,191,325',
				// 'area' => '113,321,121,364',
				// 'walls' => array(
				// 	'114,349,120,407',
				// 	),
				// 'url' => $url . 'Raum_W_tuerlaibungen.gif',
				// 'fileName' => 'Raum_W_tuerlaibunglinksunten.csv',
				// 'setting' => 'outer',
				// 'cut' => array(
				// 	'x2' => '184'
				// 	)
				// ),
				// 	
				// 'Raum_Y' => array(
				// 	'mainArea' => '307,285,319,306',
				// 	'area' => '166,134,245,250',
				// 	'walls' => array(
				// 		'166,16,245,134',
				// 		'245,134,361,250',
				// 		'166,250,245,369',
				// 		'52,134,166,250',
				// 		),
				// 	'url' => $url . 'Raum_Y.gif',
				// 	'fileName' => 'Raum_Y.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(
				// 		'x2' => '359'
				// 		)
				// 	),
				// 'Raum_Y_aussentuer_rechts' => array(
				// 	'mainArea' => '317,284,324,297',
				// 	'area' => '361,131,372,210',
				// 	'walls' => array(
				// 		'360,209,374,295',
				// 		'371,131,477,210'
				// 		),
				// 	'url' => $url . 'Raum_Y_3.gif',
				// 	'fileName' => 'Raum_Y_aussentuer_rechts.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'x1' => '359'
				// 		),
				// 	),
				// 'Raum_Y_aussentuer_links' => array(
				// 	'mainArea' => '297,284,308,298',
				// 	'area' => '141,269,154,323',
				// 	'walls' => array(
				// 		'18,269,142,346',
				// 		'141,322,152,408'
				// 		),
				// 	'url' => $url . 'Raum_Y_3.gif',
				// 	'fileName' => 'Raum_Y_aussentuer_links.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'x2' => '160',
				// 		'y1' => '259'
				// 		),
				// 	),
				// 	
				// 'Raum_Z' => array(
				// 	'mainArea' => '168,268,181,299',
				// 	'area' => '137,132,195,250',
				// 	'walls' => array(
				// 		'137,10,195,132',
				// 		'195,132,314,250',
				// 		'137,250,213,376',
				// 		'16,132,137,250',
				// 		),
				// 	'url' => $url . 'Raum_Z.gif',
				// 	'fileName' => 'Raum_Z.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(
				// 		'x2' => '323'
				// 		)
				// 	),
				// 'Raum_Z_aussentuer' => array(
				// 	'mainArea' => '180,291,189,299',
				// 	'area' => '313,210,333,260',
				// 	'walls' => array(
				// 		'332,213,392,257'
				// 		),
				// 	'url' => $url . 'Raum_Z.gif',
				// 	'fileName' => 'Raum_Z_aussentuer.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'x1' => '323',
				// 		),
				// 	),
					
				// 'Wand_B' => array(
				// 	'mainArea' => '221,113,266,191',
				// 	'area' => '133,117,290,325',
				// 	'walls' => array(
				// 		'133,9,290,117',
				// 		'290,117,399,325',
				// 		'24,117,133,325',
				// 		),
				// 	'url' => $url . 'Wand_B_2.gif',
				// 	'fileName' => 'Wand_B.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
						
				// 		),
				// 	),
				// 	
				// 'Wand_C' => array(
				// 	'mainArea' => '208,101,278,186',
				// 	'area' => '202,218,549,650',
				// 	'walls' => array(
				// 		'202,63,549,218',
				// 		'549,218,705,650',
				// 		'202,650,549,800',
				// 		'50,218,202,650',
				// 		),
				// 	'url' => $url . 'Wand_C_2.gif',
				// 	'fileName' => 'Wand_C.csv',
				// 	'setting' => 'inner',
				// 	'cut' => array(
						
				// 		),
				// 	),
				// 	
				// 'Wand_F' => array(
				// 	'mainArea' => '149,50,334,349',
				// 	'area' => '206,170,543,686',
				// 	'walls' => array(
				// 		'206,35,543,170',
				// 		'543,170,677,686',
				// 		'206,686,543,685',
				// 		'71,170,206,686',
				// 		),
				// 	'url' => $url . 'Wand_F_2.gif',
				// 	'fileName' => 'Wand_F.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		),
				// 	),
				// 	
				// 'Wand_G_links' => array(
				// 	'mainArea' => '132,348,152,451',
				// 	'area' => '219,215,277,456',
				// 	'walls' => array(
				// 		'219,46,375,215',
				// 		'375,215,546,456',
				// 		'219,456,375,456',
				// 		'47,215,219,456',
				// 		),
				// 	'url' => $url . 'Wand_G_2.gif',
				// 	'fileName' => 'Wand_G_links.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'x2' => '290',
				// 		),
				// 	),
				// 'Wand_G_rechts' => array(
				// 	'mainArea' => '332,348,352,451',
				// 	'area' => '318,215,375,457',
				// 	'walls' => array(
				// 		'219,46,375,215',
				// 		'375,215,546,456',
				// 		'219,456,375,456',
				// 		'47,215,219,456',
				// 		),
				// 	'url' => $url . 'Wand_G_2.gif',
				// 	'fileName' => 'Wand_G_rechts.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'x1' => '290',
				// 		),
				// 	),
				// 	
				// 'Tuer_Hs_Js_1' => array(
				// 	'mainArea' => '114,657,123,665',
				// 	'area' => '180,118,190,213',
				// 	'walls' => array(
				// 		'189,118,324,213',
				// 		'55,118,181,214',
				// 		),
				// 	'url' => $url . 'Tuer_Hs_Js_1_3.gif',
				// 	'fileName' => 'Tuer_Hs_Js_1.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'y2' => '213'
				// 		),
				// 	),

				// 'Tuer_Hs_Js_1_tuerlaibungen' => array(
				// 	'mainArea' => '114,657,123,665',
				// 	'area' => '180,118,190,190',
				// 	'walls' => array(
				// 		'180,189,190,284'
				// 		),
				// 	'url' => $url . 'Tuer_Hs_Js_1_3.gif',
				// 	'fileName' => 'Tuer_Hs_Js_1_tuerlaibung.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'y1' => '213'
				// 		),
				// 	),
				// 'Tuer_Hs_Js_1s' => array(
				// 	'mainArea' => '361,633,370,649',
				// 	'area' => '302,98,325,216',
				// 	'walls' => array(
				// 		'324,98,463,216',
				// 		'168,98,303,215'
				// 		),
				// 	'url' => $url . 'Tuer_Hs_Js_1s_3.gif',
				// 	'fileName' => 'Tuer_Hs_Js_1s.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'y1' => '98',
				// 		'y2' => '214'
				// 		),
				// 	),
				// 'Tuer_Hs_Js_1s_tuerlaibungen' => array(
				// 	'mainArea' => '361,633,370,649',
				// 	'area' => '302,122,325,192',
				// 	'walls' => array(
				// 		'302,28,325,123',
				// 		'302,191,325,286'
				// 		),
				// 	'url' => $url . 'Tuer_Hs_Js_1s_4.gif',
				// 	'fileName' => 'Tuer_Hs_Js_1s_tuerlaibungen.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'x1' => '301',
				// 		'x2' => '325'
				// 		),
				// 	),
				// 'Tuer_Hs_Js_2' => array(
				// 	'mainArea' => '114,451,123,460',
				// 	'area' => '217,127,232,223',
				// 	'walls' => array(
				// 		'231,128,347,223',
				// 		'101,127,218,223'
				// 		),
				// 	'url' => $url . 'Tuer_Hs_Js_2_2.gif',
				// 	'fileName' => 'Tuer_Hs_Js_2.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		),
				// 	),
				// 	
				// 'Tuer_Is_Js_1' => array(
				// 	'mainArea' => '361,277,370,288',
				// 	'area' => '255,106,278,224',
				// 	'walls' => array(
				// 		'277,106,398,224',
				// 		'138,106,256,223'
				// 		),
				// 	'url' => $url . 'Tuer_Is_Js_1_2.gif',
				// 	'fileName' => 'Tuer_Is_Js_1.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'y2' => '223'
				// 		),
				// 	),
				// 'Tuer_Is_Js_1_tuerlaibungen' => array(
				// 	'mainArea' => '361,277,370,288',
				// 	'area' => '255,106,278,200',
				// 	'walls' => array(
				// 		'255,199,278,294',
				// 		),
				// 	'url' => $url . 'Tuer_Is_Js_1_2.gif',
				// 	'fileName' => 'Tuer_Is_Js_1_tuerlaibungen.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'y1' => '223'
				// 		),
				// 	),
				// 'sued' => array(
				// 	'mainArea' => '213,821,274,880',
				// 	'area' => '554,422,685,528',
				// 	'walls' => array(
				// 		'555,282,685,424',
				// 		'554,527,684,664'
				// 		),
				// 	'url' => $url . 'sued_3.gif',
				// 	'fileName' => 'south.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'x1' => '555',
				// 		'x2' => '684',
				// 		'y2' => '663'
				// 		),
				// 	),
				// 'sued_tuerlaibungen' => array(
				// 	'mainArea' => '235,821,254,880',
				// 	'area' => '583,422,655,528',
				// 	'walls' => array(
				// 		'654,422,769,527',
				// 		'468,423,584,527'
				// 		),
				// 	'url' => $url . 'sued_2.gif',
				// 	'fileName' => 'south_tuerlaibungen.csv',
				// 	'setting' => 'outer',
				// 	'cut' => array(
				// 		'y1' => '421',
				// 		'y2' => '528',
				// 		),
				// 	),
	);


// in these lists you can specify different parameters for data which cannot be determined automatically
$lists = array(
'angleOfViewList' => array ( // mark links (for image maps) or coordinates (for images) manually to an angle of view
					'90degrees' => array(
						'Chassinat/5_250.jpg',
						'Chassinat/5_220.jpg',
						'Chassinat/5_247.jpg',
						'Chassinat/5_244.jpg',
						'Chassinat/5_241.jpg',
						'Chassinat/5_238.jpg',
						'Chassinat/5_235.jpg',
						'Chassinat/5_232.jpg',
						'Chassinat/5_229.jpg',
						'Chassinat/5_226.jpg',
						'Chassinat/5_223.jpg',
						'Chassinat/5_220.jpg',
						'Chassinat/5_216.jpg',
						'Chassinat/5_213.jpg',
						'Chassinat/5_209.jpg',
						'Chassinat/5_205.jpg',
						'Chassinat/5_201.jpg',
						'Chassinat/5_253.jpg',
						'Chassinat/5_257.jpg',
						'Chassinat/5_261.jpg',
						'Chassinat/5_264.jpg',
						'Chassinat/5_268.jpg',
						'Chassinat/5_271.jpg',
						'Chassinat/5_274.jpg',
						'Chassinat/5_277.jpg',
						'Chassinat/5_280.jpg',
						'Chassinat/5_283.jpg',
						'Chassinat/5_286.jpg',
						'Chassinat/5_289.jpg',
						'Chassinat/5_292.jpg',
						'Chassinat/5_295.jpg',
						'Chassinat/5_298.jpg',
						'Chassinat/5_301.jpg',
						//Raum V
						// '159,295,197,321',
						//Raum W
						// '193,225,208,257',
						// '255,225,270,257',
						// '327,225,342,257',
						// '388,225,403,257',
						// '194,289,209,321',
						// '255,289,270,321',
						// '327,289,342,321',
						// '388,289,403,321',
						// '194,352,209,384',
						// '255,352,270,384',
						// '327,352,342,384',
						// '388,352,403,384',
						//Raum C
						// '204,171,216,185',
						// '250,171,262,185',
						// '296,171,308,185',
						// '356,171,368,197',
						// '402,171,414,185',
						// '448,171,460,185',
						// '204,185,216,197',
						// '250,185,262,197',
						// '296,185,308,197',
						// '402,185,414,197',
						// '448,185,460,197',
						// '204,227,216,241',
						// '250,227,262,241',
						// '296,227,308,241',
						// '356,227,368,253',
						// '402,227,414,241',
						// '448,227,460,241',
						// '204,241,216,253',
						// '250,241,262,253',
						// '296,241,308,253',
						// '369,241,381,253',
						// '402,241,414,253',
						// '448,241,460,253',
						//Raum C Architrave
						// '204,142,216,208',
						// '250,142,262,208',
						// '296,142,308,208',
						// '356,142,368,208',
						// '402,142,414,208',
						// '448,142,460,208',
						// '204,212,216,285',
						// '250,212,262,285',
						// '296,212,308,285',
						// '356,212,368,285',
						// '402,212,414,285',
						// '448,212,460,285',
						),
					'270degrees' => array(
						'Chassinat/5_251.jpg',
						'Chassinat/5_248.jpg',
						'Chassinat/5_245.jpg',
						'Chassinat/5_242.jpg',
						'Chassinat/5_239.jpg',
						'Chassinat/5_236.jpg',
						'Chassinat/5_233.jpg',
						'Chassinat/5_230.jpg',
						'Chassinat/5_227.jpg',
						'Chassinat/5_224.jpg',
						'Chassinat/5_221.jpg',
						'Chassinat/5_217.jpg',
						'Chassinat/5_214.jpg',
						'Chassinat/5_210.jpg',
						'Chassinat/5_206.jpg',
						'Chassinat/5_202.jpg',
						'Chassinat/5_254.jpg',
						'Chassinat/5_258.jpg',
						'Chassinat/5_265.jpg',
						'Chassinat/5_269.jpg',
						'Chassinat/5_272.jpg',
						'Chassinat/5_275.jpg',
						'Chassinat/5_278.jpg',
						'Chassinat/5_281.jpg',
						'Chassinat/5_284.jpg',
						'Chassinat/5_287.jpg',
						'Chassinat/5_290.jpg',
						'Chassinat/5_293.jpg',
						'Chassinat/5_296.jpg',
						'Chassinat/5_299.jpg',
						'Chassinat/5_302.jpg',
						//Raum W
						// '208,225,224,257',
						// '270,225,286,257',
						// '342,225,358,257',
						// '403,225,419,257',
						// '209,289,225,321',
						// '270,289,286,321',
						// '342,289,358,321',
						// '403,289,419,321',
						// '209,352,225,384',
						// '270,352,286,384',
						// '342,352,358,384',
						// '403,352,419,384',
						// Raum C
						// '217,171,229,185',
						// '263,171,275,185',
						// '309,171,321,197',
						// '369,171,381,185',
						// '415,171,427,185',
						// '461,171,473,185',
						// '217,185,229,197',
						// '263,185,275,197',
						// '369,185,381,197',
						// '415,185,427,197',
						// '461,185,473,197',
						// '217,227,229,241',
						// '263,227,275,241',
						// '309,227,321,253',
						// '369,227,381,241',
						// '415,227,427,241',
						// '461,227,473,241',
						// '217,241,229,253',
						// '263,241,275,253',
						// '415,241,427,253',
						// '461,241,473,253',
						// Raum C Architrave
						// '217,142,229,208',
						// '263,142,275,208',
						// '309,142,321,208',
						// '369,142,381,208',
						// '415,142,427,208',
						// '461,142,473,208',
						// '217,212,229,285',
						// '263,212,275,285',
						// '309,212,321,285',
						// '369,212,381,285',
						// '415,212,427,285',
						// '461,212,473,285',
					),
				),
'exceptionList' => array ( // does not calculate these data
						'Chassinat/8_029.jpg',
						'Chassinat/8_028.jpg',
						'Chassinat/8_028.jpg',
						'Chassinat/8_026.jpg',
						'Chassinat/8_025.jpg',
						'Chassinat/8_057.jpg',
						'Chassinat/8_055.jpg',
						'Chassinat/8_054.jpg',
						'Chassinat/8_053.jpg',
						'Chassinat/8_052.jpg',
						'Chassinat/8_065.jpg',
						'Chassinat/8_064.jpg',
						'Chassinat/8_063.jpg',
						'Chassinat/8_062.jpg',
						'Chassinat/8_060.jpg',
						'Chassinat/8_037.jpg',
						'Chassinat/8_036.jpg',
						'Chassinat/8_035.jpg',
						'Chassinat/8_034.jpg',
						'Chassinat/8_032.jpg',
						//Raum_As_aussentuer
						//'26,158,59,168',
						//Raum_A
						// '153,463,173,485',
						// '229,463,249,485',
						// '153,486,173,509',
						// '229,486,249,509',
						// '124,501,151,531',
						// '251,501,278,531',
						// '153,510,173,531',
						// '229,510,249,531',
						//Raum B
						// '212,18,227,31',
						// '212,38,227,73',
						// '212,33,227,36'

						),
/*
	for image maps only: if you want to automatically convert polygons to rectangles 
	you can specify	the coordinates of the wall in relation to the old wall
 */
'smallWallsList' => array(  
						//pylon
						'149,305,547,485' => '187,304,505,485',
						'114,85,547,265' => '185,85,504,266',
						'503,244,674,326' => '502,264,674,306',
						'17,243,189,328' => '18,263,190,307'
						)
);

?>