<?php

class CdppSipadRestServiceClient
{

// Connection
private $host = "";
private $client_id = "";
private $client_secret = "";
private $scope = "";
private $username = "";
private $password = "";

// Port services
private $portAdm = "";
private $portCmd = "";
private $portCons = "";
private $portCnx = "";
private $portUserMngt = "";
private $portWorkspace = "";
private $portCmdTele = "";
private $portWorkspaceTele = "";
private $portCdpp = "";
private $portIngestion = "";
private $hostRest = "";

// Services
private $serviceAdm = "";
private $serviceCmd = "";
private $serviceCons = "";
private $serviceCnx = "";
private $serviceUserMngt = "";
private $serviceWorkspace = "";
private $serviceCmdTele = "";
private $serviceWorkspaceTele = "";
private $serviceCdpp = "";
private $serviceIngestion = "";

// type_accept
private $acceptTypeJson = "";
private $acceptTypeXml = "";

// Result files path
private $result_path = "";

// Properties for debug mode
private $debug_mode = false;
private $debug_path = "./";

// Token obtained after service connection
private $token      = "";

public function __construct($tdb_conf, $result_path)
{
// Connection
	$this->host          = $tdb_conf['SO1_connection']['vHostIp'];
	$this->client_id     = $tdb_conf['SO1_connection']['vClientId'];
	$this->client_secret = $tdb_conf['SO1_connection']['vClientSecret'];
	$this->scope         = $tdb_conf['SO1_connection']['vProject'];
	$this->username      = $tdb_conf['SO1_connection']['vUser'];
	$this->password      = $tdb_conf['SO1_connection']['vPassword'];

	$this->portAdm        = $tdb_conf['SO1_connection']['vPortAdm'];
	$this->portCmd        = $tdb_conf['SO1_connection']['vPortCmd'];
	$this->portCons       = $tdb_conf['SO1_connection']['vPortCons'];
	$this->portCnx        = $tdb_conf['SO1_connection']['vPortCnx'];
	$this->portUserMgnt   = $tdb_conf['SO1_connection']['vPortUserMgnt'];
	$this->portWorkspace  = $tdb_conf['SO1_connection']['vPortWorkspace'];
	$this->portWorkspaceTele   = $tdb_conf['SO1_connection']['vPortWorkspaceTele'];
	$this->portCdpp       = $tdb_conf['SO1_connection']['vPortCdpp'];
	$this->portIngestion  = $tdb_conf['SO1_connection']['vPortIngestion'];
	$this->hostRest       = $tdb_conf['SO1_connection']['vHostRest'];

// Services
	$this->serviceAdm       = $this->host.":".$this->portAdm."/administration-".$this->hostRest;
	$this->serviceCmd       = $this->host.":".$this->portCmd."/command-".$this->hostRest."/".$this->scope."/command";
	$this->serviceCons      = $this->host.":".$this->portCons."/consultation-".$this->hostRest."/".$this->scope."/consultation";
	$this->serviceCnx       = $this->host.":".$this->portCnx."/userauthenticate-".$this->hostRest;
	$this->serviceUserMngt  = $this->host.":".$this->portUserMgnt."/usermanagement-".$this->hostRest."/usermanagement";
	$this->serviceWorkspace = $this->host.":".$this->portWorkspace."/userworkspace-".$this->hostRest."/userworkspace";
	$this->serviceCmdTele   = $this->portCmdTele;
	$this->serviceWorkspaceTele = $this->portWorkspaceTele;
	$this->serviceCdpp      = $this->host.":".$this->portCdpp."/cdpp-".$this->hostRest."/".$this->scope."/cdpp";
	$this->serviceIngestion = $this->host.":".$this->portIngestion."/ingestion-".$this->hostRest;

// Type_accept
	$this->acceptTypeJson = $tdb_conf['type_accept']['vAcceptTypeJson'];
	$this->acceptTypeXml  = $tdb_conf['type_accept']['vAcceptTypeXml'];

// Application
	$this->debug_mode    = $tdb_conf['application']['debug_mode'];
	$this->debug_path    = $tdb_conf['application']['debug_path'];
	$this->result_path   = $result_path;
}

public function openConnection()
{
	if ($this->token != "")
		//Already connected to the service
		return array("success" => true, "token" => $this->token);

	$url = $this->serviceCnx."/oauth/token";

	$data = array(
		"client_id"     => $this->client_id,
		"client_secret" => $this->client_secret,
		"grant_type"    => "password",
		"username"      => $this->username,
		"password"      => $this->password,
		"scope"         => $this->scope
	);

	$options = array(
		"http" => array(
			"header" => "Content-type: application /x-www-form-urlencoded",
			"method" => "POST",
			"content" => http_build_query($data)
		)
	);

	if ($this->debug_mode)
		$result_json = file_get_contents($this->debug_path."/token.json");
	else
		$result_json = $this->callRequest($url, $options);

	$file = fopen($this->result_path."/token.json","w");
	fwrite($file,$result_json);
	
	if ($result_json === FALSE)
		return array("success" => false, "message" => "Error during get token request");

	$result = json_decode($result_json);

	if (!isset($result) || !isset($result->access_token) || ($result->access_token == ""))
		return array("success" => false, "message" => "Error to parse get token request result");

	$this->token = $result->access_token;

	return array("success" => true, "token" => $this->token);
}

public function getMissionsList()
{
	if ($this->token == "")
		return array("success" => false, "message" => "Client not connected to the service");

	$url = $this->serviceCdpp."/missions";

	$options = array(
		"http" => array(
			"header" => "Authorization: Bearer ".$this->token."\r\n".
			"Accept: application/json\r\n",
			"method" => "GET"
		)
	);

	if ($this->debug_mode)
		$result_json = file_get_contents($this->debug_path."/missions.json");
	else
		$result_json = $this->callRequest($url, $options);

	if ($result_json === FALSE)
		return array("success" => false, "message" => "Error during get missions list request");

	$file = fopen($this->result_path."/missions.json","w");
	fwrite($file,$result_json);
	
	$result = json_decode($result_json);

	return array("success" => true, "missions" => $result->results);
}

public function getInstrumentsList($mission)
{
	if ($this->token == "")
		return array("success" => false, "message" => "Client not connected to the service");

	$url = $this->serviceCdpp."/missions/".rawurlencode($mission)."/instruments/";

	$options = array(
		"http" => array(
			"header" => "Authorization: Bearer ".$this->token."\r\n".
			"Accept: application/json\r\n",
			"method" => "GET"
		)
	);

	if ($this->debug_mode)
		$result_json = file_get_contents($this->debug_path."/instruments-".$mission.".json");
	else
		$result_json = $this->callRequest($url, $options);

	if ($result_json === FALSE)
		return array("success" => false, "message" => "Error during get instruments list request for ".$mission);

	$file = fopen($this->result_path."/instruments-".$mission.".json","w");
	fwrite($file,$result_json);
		
	$result = json_decode($result_json);

	return array("success" => true, "instruments" => $result->results);
}

public function getDatasetsList($mission, $instrument)
{
	if ($this->token == "")
		return array("success" => false, "message" => "Client not connected to the service");

	$data = array(
		"mission"    => $mission,
		"instrument" => $instrument
	);

	$url = $this->serviceCdpp."/datasets/?".http_build_query($data);

	$options = array(
		"http" => array(
			"header" => "Authorization: Bearer ".$this->token."\r\n".
			"Accept: application/json\r\n",
			"method" => "GET"
		)
	);

	if ($this->debug_mode)
		$result_json = file_get_contents($this->debug_path."/datasets-".$mission."-".str_replace("/","_",$instrument).".json");
	else
		$result_json = $this->callRequest($url, $options);

	if ($result_json === FALSE)
		return array("success" => false, "message" => "Error during get datasets list request for ".$mission."/".$instrument);

	$file = fopen($this->result_path."/datasets-".$mission."-".str_replace("/","_",$instrument).".json","w");
	fwrite($file,$result_json);
		
	$result = json_decode($result_json);

	return array("success" => true, "datasets" => $result->results);
}

public function getDatasetsConsultationByMission($mission)
{
	if ($this->token == "")
		return array("success" => false, "message" => "Client not connected to the service");

	$url = $this->serviceCons."/datasets?MISSION=".$mission;

	$options = array(
		"http" => array(
			"header" => "Authorization: Bearer ".$this->token."\r\n".
			"Accept: application/xml\r\n",
			"method" => "GET"
		)
	);

	if ($this->debug_mode)
		$result_xml = file_get_contents($this->debug_path."/datasets-consultation-".$mission.".xml");
	else
		$result_xml = $this->callRequest($url, $options);

	if ($result_xml === FALSE)
		return array("success" => false, "message" => "Error during datasets consultation for ".$mission);

	$file = fopen($this->result_path."/datasets-consultation-".$mission.".xml","w");
	fwrite($file,$result_xml);
		
	return array("success" => true, "datasets" => $result_xml);
}

public function getSharedEntities()
{
	if ($this->token == "")
		return array("success" => false, "message" => "Client not connected to the service");

	$url = $this->serviceCons."/sharedentities";

	$options = array(
		"http" => array(
			"header" => "Authorization: Bearer ".$this->token."\r\n".
			"Accept: application/xml\r\n",
			"method" => "GET"
		)
	);

	if ($this->debug_mode)
		$result_xml = file_get_contents($this->debug_path."/sharedentities.xml");
	else
		$result_xml = $this->callRequest($url, $options);

	if ($result_xml === FALSE)
		return array("success" => false, "message" => "Error during get shared entities request");

	$file = fopen($this->result_path."/sharedentities.xml","w");
	fwrite($file,$result_xml);
		
	return array("success" => true, "sharedentities" => $result_xml);
}

public function getDataObjectsByDatasetId($dataset_id)
{
	if ($this->token == "")
		return array("success" => false, "message" => "Client not connected to the service");

	$url = $this->serviceCons."/search/entities/";

	$data = array(
        "targetList"           => array(),
		"startPosition"        => 1,
		"maxRecords"           => -1,
		"paginatedEntity"      => "OBJECT",
		"paginatedEntityType"  => "DATA",
		"visibility"           => "IDENTIFIER",
		"objectVisibility"     => "STANDARD",
		"returnSum"            => true,
		"collectionDeepSearch" => false,
		"startNode"            => array(
			"entity" => array(
				"type" => "DATASET",
				"id"   => $dataset_id
			)
		)
	);
	
	$options = array(
		"http" => array(
			"header" => "Authorization: Bearer ".$this->token."\r\n".
			"Accept: application/json\r\n".
			"Content-Type:application/json\r\n",
			"method" => "POST",
			"content" => json_encode($data)
		)
	);

	if ($this->debug_mode)
		$result_json = file_get_contents($this->debug_path."/dataobjects-".$dataset_id.".json");
	else
		$result_json = $this->callRequest($url, $options);

	if ($result_json === FALSE)
		return array("success" => false, "message" => "Error during get data objects request");

	$file = fopen($this->result_path."/dataobjects-".$dataset_id.".json","w");
	fwrite($file,$result_json);

	$result = json_decode($result_json);

	return array("success" => true, "dataobjects" => $result->results);
}

private static function callRequest($url, $options)
{
	$context = stream_context_create($options);
	return @file_get_contents($url, false, $context);
}

};

?>
