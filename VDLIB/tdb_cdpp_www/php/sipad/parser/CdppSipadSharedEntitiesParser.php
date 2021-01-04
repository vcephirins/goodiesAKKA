<?php

require_once("CdppSipadXmlResultParserAbstract.php");

class CdppSipadSharedEntitiesParser extends CdppSipadXmlResultParserAbstract
{

function __construct()
{
	parent::__construct();
}

public function parse()
{
	if (!$this->isLoaded())
		return FALSE;
		
	$sharedentity_nodes = $this->xpath->query("//ResultRest/results/SharedEntities/SharedEntity");
	
	$mission_entities     = array();
	$experiment_entities  = array();
	$observatory_entities = array();
	$instrument_entities  = array();
	
	foreach ($sharedentity_nodes as $sharedentity_node)
	{
		//shared entity node path
		$sharedentity_node_path = $sharedentity_node->getNodePath();
	
		//Get name node and use it as id
		$name_nodes = $this->xpath->query($sharedentity_node_path."/name");
		if ($name_nodes->length != 1)
		{
			echo "[ERROR] - Shared entity without name node".PHP_EOL;
			continue;
		}
		$sharedentity_id = $name_nodes->item(0)->nodeValue;
		
		//Get attributes
		$attributes_nodes = $this->xpath->query($sharedentity_node_path."/attributes");
		if ($attributes_nodes->length != 1)
		{
			echo "[ERROR] - Shared entity without attributes node".PHP_EOL;
			continue;
		}
		$attributes_node = $attributes_nodes->item(0);
		
		if ($this->isMission($sharedentity_node))
		{
			//get mission name
			$mission_attribute_nodes = $this->xpath->query($sharedentity_node_path."/attributes/attribute[name='MISSION']");
			if ($mission_attribute_nodes->length >= 1)
			{
				$mission_name = $this->getStringAttributeValue($mission_attribute_nodes->item(0));
				if ($mission_attribute_nodes->length > 1)
					echo "[WARNING] - More than one mission node defined for the entity".PHP_EOL;
			}
			else
				$mission_name = $sharedentity_id;
				
			//get mission start date
			$startdate_attribute_nodes = $this->xpath->query($sharedentity_node_path."/attributes/attribute[name='MISSION_START_DATE']");
			if ($startdate_attribute_nodes->length >= 1)
			{
				$mission_startdate = $this->getStringAttributeValue($startdate_attribute_nodes->item(0));
				if ($startdate_attribute_nodes->length > 1)
					echo "[WARNING] - More than one start date node defined for the mission entity".PHP_EOL;
			}
			else
				$mission_startdate = "1970-01-01T00:00:00Z";
			
			$mission_entities[] = array(
				"id"         => $sharedentity_id,
				"name"       => $mission_name,
				"start_date" => $mission_startdate
			);
		}
		else if ($this->isExperiment($sharedentity_node))
		{
			//get experiment name
			$experiment_attribute_nodes = $this->xpath->query($sharedentity_node_path."/attributes/attribute[name='EXPERIMENT']");
			if ($experiment_attribute_nodes->length >= 1)
			{
				$experiment_name = $this->getStringAttributeValue($experiment_attribute_nodes->item(0));
				if ($experiment_attribute_nodes->length > 1)
					echo "[WARNING] - More than one experiment node defined for the entity".PHP_EOL;
			}
			else
				$experiment_name = $sharedentity_id;
				
			$experiment_entities[] = array(
				"id"         => $sharedentity_id,
				"name"       => $experiment_name
			);
		}
		else if ($this->isObservatory($sharedentity_node))
		{
			//get observatory name
			$observatory_attribute_nodes = $this->xpath->query($sharedentity_node_path."/attributes/attribute[name='OBSERVATORY']");
			if ($observatory_attribute_nodes->length >= 1)
			{
				$observatory_name = $this->getStringAttributeValue($observatory_attribute_nodes->item(0));
				if ($observatory_attribute_nodes->length > 1)
					echo "[WARNING] - More than one observatory node defined for the entity".PHP_EOL;
			}
			else
				$observatory_name = $sharedentity_id;
				
			//get observatory start date
			$startdate_attribute_nodes = $this->xpath->query($sharedentity_node_path."/attributes/attribute[name='OBSERVATORY_START_DATE']");
			if ($startdate_attribute_nodes->length >= 1)
			{
				$observatory_startdate = $this->getStringAttributeValue($startdate_attribute_nodes->item(0));
				if ($startdate_attribute_nodes->length > 1)
					echo "[WARNING] - More than one start date node defined for the observatory entity".PHP_EOL;
			}
			else
				$observatory_startdate = "1970-01-01T00:00:00Z";
				
			//get observatory stop date
			$stopdate_attribute_nodes = $this->xpath->query($sharedentity_node_path."/attributes/attribute[name='OBSERVATORY_STOP_DATE']");
			if ($stopdate_attribute_nodes->length >= 1)
			{
				$observatory_stopdate = $this->getStringAttributeValue($stopdate_attribute_nodes->item(0));
				if ($stopdate_attribute_nodes->length > 1)
					echo "[WARNING] - More than one start date node defined for the observatory entity".PHP_EOL;
			}
			else
				$observatory_stopdate = "1970-01-01T00:00:00Z";
				
			//get observatory regions
			$region_attribute_nodes = $this->xpath->query($sharedentity_node_path."/attributes/attribute[name='OBSERVATORY_REGION']");
			$observatory_regions = array();
			foreach ($region_attribute_nodes as $region_attribute_node)
			{
				$region = $this->getStringAttributeValue($region_attribute_node);
				if (!in_array($region,$observatory_regions))
					$observatory_regions[] = $region;
			}
			
			$observatory_entities[] = array(
				"id"         => $sharedentity_id,
				"name"       => $observatory_name,
				"start_date" => $observatory_startdate,
				"stop_date"  => $observatory_stopdate,
				"regions"    => $observatory_regions
			);
		}
		else if ($this->isInstrument($sharedentity_node))
		{
			//get instrument name
			$instrument_attribute_nodes = $this->xpath->query($sharedentity_node_path."/attributes/attribute[name='INSTRUMENT']");
			if ($instrument_attribute_nodes->length >= 1)
			{
				$instrument_name = $this->getStringAttributeValue($instrument_attribute_nodes->item(0));
				if ($instrument_attribute_nodes->length > 1)
					echo "[WARNING] - More than one instrument node defined for the entity".PHP_EOL;
			}
			else
				$instrument_name = $sharedentity_id;
				
			//get measurement types
			$measurementtype_attribute_nodes = $this->xpath->query($sharedentity_node_path."/attributes/attribute[name='MEASUREMENT_TYPE']");
			$instrument_measurementtypes = array();
			foreach ($measurementtype_attribute_nodes as $measurementtype_attribute_node)
			{
				$measurementtype = $this->getStringAttributeValue($measurementtype_attribute_node);
				if (!in_array($measurementtype,$instrument_measurementtypes))
					$instrument_measurementtypes[] = $measurementtype;
			}
			
			//get instrument types
			$instrumenttype_attribute_nodes = $this->xpath->query($sharedentity_node_path."/attributes/attribute[name='INSTRUMENT_TYPE']");
			$instrument_types = array();
			foreach ($instrumenttype_attribute_nodes as $instrumenttype_attribute_node)
			{
				$instrumenttype = $this->getStringAttributeValue($instrumenttype_attribute_node);
				if (!in_array($instrumenttype,$instrument_types))
					$instrument_types[] = $instrumenttype;
			}
			
			$instrument_entities[] = array(
				"id"                => $sharedentity_id,
				"name"              => $instrument_name,
				"instrument_types"  => $instrument_types,
				"measurement_types" => $instrument_measurementtypes
			);
		}
		else
		{
			echo "[ERROR] - Unknown shared entity type".PHP_EOL;
			continue;
		}
	}
		
	return array(
		"missions"      => $mission_entities,
		"experiments"   => $experiment_entities,
		"observatories" => $observatory_entities,
		"instruments"   => $instrument_entities
	);	
}

private function isMission($sharedentity_node)
{
	$sharedentity_node_path = $sharedentity_node->getNodePath();
	$mission_nodes = $this->xpath->query($sharedentity_node_path."/attributes/attribute[name='MISSION']");
	return ($mission_nodes->length > 0);
}

private function isExperiment($sharedentity_node)
{
	$sharedentity_node_path = $sharedentity_node->getNodePath();
	$experiment_nodes = $this->xpath->query($sharedentity_node_path."/attributes/attribute[name='EXPERIMENT']");
	return ($experiment_nodes->length > 0);
}

private function isObservatory($sharedentity_node)
{
	$sharedentity_node_path = $sharedentity_node->getNodePath();
	$observatory_nodes = $this->xpath->query($sharedentity_node_path."/attributes/attribute[name='OBSERVATORY']");
	return ($observatory_nodes->length > 0);
}

private function isInstrument($sharedentity_node)
{
	$sharedentity_node_path = $sharedentity_node->getNodePath();
	$instrument_nodes = $this->xpath->query($sharedentity_node_path."/attributes/attribute[name='INSTRUMENT']");
	return ($instrument_nodes->length > 0);
}

};

?>