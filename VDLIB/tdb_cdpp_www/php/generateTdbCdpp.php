<?php
// Set time zone to UTC
date_default_timezone_set('UTC');

// Load configuration file
$tdb_conf = parse_ini_file("../conf/tdbcdpp.ini", true);

require_once("sipad/service/CdppSipadRestServiceClient.php");
require_once("sipad/parser/CdppSipadDatasetConsultationParser.php");
require_once("sipad/parser/CdppSipadSharedEntitiesParser.php");
require_once("tree/TreeBuilderByMission.php");
require_once("database/DatabaseManager.php");

//Create a new session
DatabaseManager::getInstance()->setPath($tdb_conf['application']['database_path']);
if (!DatabaseManager::getInstance()->createNewSession())
{
	echo "[ERROR] - Cannot create a new session".PHP_EOL;
	exit(1);
}

$client = new CdppSipadRestServiceClient($tdb_conf, DatabaseManager::getInstance()->getSessionSipadServiceDataPath());

//Establish the connection to the service
echo "[INFO] - Open connection to SIPAD REST service".PHP_EOL;
$resServiceConnection = $client->openConnection();
if (!$resServiceConnection["success"])
{
	echo "[ERROR] - ".$resServiceConnection["message"].PHP_EOL;
	exit(1);
}

//Get missions list
echo "[INFO] - Get missions list".PHP_EOL;
$resServiceMissions = $client->getMissionsList();
if (!$resServiceMissions["success"])
{
	echo "[ERROR] - ".$resServiceMissions["message"].PHP_EOL;
	exit(1);
}

//Get shared entities definition
echo "[INFO] - Get shared entities".PHP_EOL;
$resServiceSharedEntities = $client->getSharedEntities();
if (!$resServiceSharedEntities["success"])
{
	echo "[ERROR] - ".$resServiceSharedEntities["message"].PHP_EOL;
	exit(1);
}

//Parse shared entities
echo "[INFO] - Parse shared entities".PHP_EOL;
$sharedentitiesParser = new CdppSipadSharedEntitiesParser();
if (!$sharedentitiesParser->loadFromString($resServiceSharedEntities["sharedentities"]))
{
	echo "[ERROR] - Cannot load shared entities".PHP_EOL;
	exit(1);
}

$sharedEntities = $sharedentitiesParser->parse();

//Get and parse datasets definition by missions
$datasets = array();
$datasetsParser = new CdppSipadDatasetsConsultationParser($sharedEntities);
foreach ($resServiceMissions["missions"] as $missionName)
{
		continue;
	if ($missionName == "ISEE3/ICE")
	{
		echo "[WARNING] - Skip mission ".$missionName.PHP_EOL;
		continue;
	}
	
	//Retrieve mission id
	$mission_id = "";
	foreach ($sharedEntities["missions"] as $mission)
	{
		if ($missionName == $mission["name"])
		{
			$mission_id = $mission["id"];
			break;
		}
	}
	if ($mission_id == "")
	{
		echo "[ERROR] - Cannot retrieve mission id for ".$missionName.PHP_EOL;
		continue;
	}

	//Get datasets
	echo "[INFO] - Get datasets consultation for mission ".$missionName.PHP_EOL;
	$resServiceDatasets = $client->getDatasetsConsultationByMission($missionName);
	if (!$resServiceDatasets["success"])
	{
		echo "[ERROR] - ".$resServiceDatasets["message"].PHP_EOL;
		continue;
	}
	
	//Parse datasets
	echo "[INFO] - Parse datasets consultation for mission ".$missionName.PHP_EOL;
	if (!$datasetsParser->loadFromString($resServiceDatasets["datasets"]))
	{
		echo "[ERROR] - Cannot load datasets consultation result for mission ".$missionName.PHP_EOL;
		continue;
	}
	$datasetsParser->setMissionId($mission_id);
	
	//Merge datasets in result array 
	$datasets = array_merge($datasets, $datasetsParser->parse());
}

//Build tree by mission
$treeBuilder = new TreeBuilderByMission($datasets, $sharedEntities);
//Save tree by mission
$handle = fopen(DatabaseManager::getInstance()->getSessionTreePath()."tree_by_mission.json","w");
fwrite($handle,json_encode($treeBuilder->build()));

//Get data objects for all datasets
foreach ($datasets as $dataset)
{
	$resServiceDataObjects = $client->getDataObjectsByDatasetId($dataset["id"]);
	if (!$resServiceDataObjects["success"])
	{
		echo "[ERROR] - ".$resServiceDataObjects["message"].PHP_EOL;
		continue;
	}
}

//Todo - close session

?>
