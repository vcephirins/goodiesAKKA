<?php

require_once("CdppSipadXmlResultParserAbstract.php");

class CdppSipadDatasetsConsultationParser extends CdppSipadXmlResultParserAbstract
{
private $sharedEntities = NULL;
private $missionId = "";

function __construct($sharedEntities)
{
	parent::__construct();
	$this->sharedEntities = $sharedEntities;
}

public function setMissionId($missionId)
{
	$this->missionId = $missionId;
}

public function parse()
{
	if (!$this->isLoaded())
		return FALSE;

	$dataset_nodes = $this->xpath->query("//ResultRest/results/Sets/Set");

	$datasets_list = array();
	foreach ($dataset_nodes as $dataset_node)
	{
		//dataset node path
		$dataset_node_path = $dataset_node->getNodePath();
	
		//get id
		$id_nodes = $this->xpath->query($dataset_node_path."/id");
		if ($id_nodes->length != 1)
		{
			echo "[ERROR] - Dataset without id".PHP_EOL;
			continue;
		}
		$dataset_id = $id_nodes->item(0)->nodeValue;
		
		//get label
		$label_nodes = $this->xpath->query($dataset_node_path."/label");
		if ($label_nodes->length != 1)
		{
			echo "[ERROR] - Dataset without name".PHP_EOL;
			continue;
		}
		$dataset_label = $label_nodes->item(0)->nodeValue;
		
		//get totalNumberOfObjects
		$nbobj_nodes = $this->xpath->query($dataset_node_path."/totalNumberOfObjects");
		if ($nbobj_nodes->length != 1)
		{
			echo "[ERROR] - Dataset without totalNumberOfObjects".PHP_EOL;
			continue;
		}
		$dataset_nbobj = $nbobj_nodes->item(0)->nodeValue;
		
		//get size
		$size_nodes = $this->xpath->query($dataset_node_path."/size");
		if ($size_nodes->length != 1)
		{
			//echo "[WARNING] - Dataset without size".PHP_EOL;
			$dataset_size = 0;
		}
		else
			$dataset_size = $size_nodes->item(0)->nodeValue;
		
		//get experiment id if exist
		$experiment_attribute_nodes = $this->xpath->query($dataset_node_path."/attributes/attribute[name='EXPERIMENT']");
		$experiment_id = "";
		if ($experiment_attribute_nodes->length >= 1)
		{
			$experiment_name = $this->getStringAttributeValue($experiment_attribute_nodes->item(0));
			if ($experiment_attribute_nodes->length > 1)
				echo "[WARNING] - More than one experiment node defined for the dataset".PHP_EOL;
			foreach ($this->sharedEntities["experiments"] as $experiment)
			{
				if ($experiment_name == $experiment["name"])
				{
					$experiment_id = $experiment["id"];
					break;
				}
			}
		}
		
		//get instruments if exist
		$instruments_id_list = array();
		$instrument_attribute_nodes = $this->xpath->query($dataset_node_path."/attributes/attribute[name='INSTRUMENT']");
		if ($instrument_attribute_nodes->length >= 1)
		{
			$instruments_name_list = $this->getStringListAttributeValue($instrument_attribute_nodes->item(0));
			if ($instrument_attribute_nodes->length > 1)
				echo "[WARNING] - More than one instrument node defined for the dataset".PHP_EOL;
			foreach ($instruments_name_list as $instrument_name)
			{
				foreach ($this->sharedEntities["instruments"] as $instrument)
				{
					if ($instrument_name == $instrument["name"])
					{
						$instruments_id_list[] = $instrument["id"];
						break;
					}
				}
			}
		}
		
		//get observatory if exist
		$observatory_attribute_nodes = $this->xpath->query($dataset_node_path."/attributes/attribute[name='OBSERVATORY']");
		$observatory_id = "";
		if ($observatory_attribute_nodes->length >= 1)
		{
			$observatory_name = $this->getStringAttributeValue($observatory_attribute_nodes->item(0));
			if ($observatory_attribute_nodes->length > 1)
				echo "[WARNING] - More than one observatory node defined for the dataset".PHP_EOL;
			foreach ($this->sharedEntities["observatories"] as $observatory)
			{
				if ($observatory_name == $observatory["name"])
				{
					$observatory_id = $observatory["id"];
					break;
				}
			}
		}
		
		$datasets_list[] = array(
			"type"             => "dataset",
			"id"               => $dataset_id,
			"name"             => $dataset_label,
			"nb_objects"       => $dataset_nbobj,
			"size"             => $dataset_size,
			"mission_id"       => $this->missionId,
			"observatory_id"   => $observatory_id,
			"experiment_id"    => $experiment_id,
			"instruments_id"   => $instruments_id_list
		);
	}
	
	return $datasets_list;
}

};

?>