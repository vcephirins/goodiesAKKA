<?php

require_once("TreeBuilderAbstract.php");
require_once("TreeNodeObject.php");

class TreeBuilderByMission extends TreeBuilderAbstract
{
function __construct($datasets, $sharedEntities)
{
	parent::__construct($datasets, $sharedEntities);
}

public function build()
{
	$rootNode = new TreeNodeObject("ROOT_BY_MISSION", "By Missions", "root");
	
	foreach($this->datasets as $dataset)
	{
		//Get mission info
		$mission_info = $this->getMissionInfoFromId($dataset["mission_id"]);
		if ($mission_info == NULL)
		{
			echo "[ERROR] - Unknown mission for dataset ".$dataset["id"].PHP_EOL;
			continue;
		}
		
		//Get observatory info
		$observatory_info = NULL;
		if ($dataset["observatory_id"] != "")
		{
			$observatory_info = $this->getObservatoryInfoFromId($dataset["observatory_id"]);
			if ($observatory_info == NULL)
				echo "[ERROR] - Unknown observatory for dataset ".$dataset["id"].PHP_EOL;
		}
		
		//Get experiment info
		$experiment_info = NULL;
		if ($dataset["experiment_id"] != "")
		{
			$experiment_info = $this->getExperimentInfoFromId($dataset["experiment_id"]);
			if ($experiment_info == NULL)
				echo "[ERROR] - Unknown experiment for dataset ".$dataset["id"].PHP_EOL;
		}
		
		//Get instruments info
		$instruments_info = array();
		foreach ($dataset["instruments_id"] as $instrument_id)
		{
			$instrument_info = $this->getInstrumentInfoFromId($instrument_id);
			if ($instrument_info == NULL)
				echo "[ERROR] - Unknown instrument for dataset ".$dataset["id"].PHP_EOL;
			else
				$instruments_info[$instrument_id] = $instrument_info;
		}
		
		//Get mission node
		$missionNode = $rootNode->getChildById($mission_info["id"]);
		if (!isset($missionNode))
		{
			//Create mission node
			$missionNode = new TreeNodeObject($mission_info["id"], $mission_info["name"], "mission");
			$rootNode->addChild($missionNode);
		}
		
		//Get observatory node
		$observatoryNode = NULL;
		if ($observatory_info != NULL)
		{
			$observatoryNode = $missionNode->getChildById($missionNode->getId()."_".$observatory_info["id"]);
			if (!isset($observatoryNode))
			{
				//Create observatory node
				$observatoryNode = new TreeNodeObject($missionNode->getId()."_".$observatory_info["id"], $observatory_info["name"], "observatory");
				$missionNode->addChild($observatoryNode);
			}
		}
		
		//Get experiment node
		$experimentNode = NULL;
		if ($experiment_info != NULL)
		{
			if ($observatory_info != NULL)
				$experimentNode = $observatoryNode->getChildById($observatoryNode->getId()."_".$experiment_info["id"]);
			else
				$experimentNode = $missionNode->getChildById($missionNode->getId()."_".$experiment_info["id"]);
			if (!isset($experimentNode))
			{
				//Create experiment node
				if ($observatory_info != NULL)
				{
					$experimentNode = new TreeNodeObject($observatoryNode->getId()."_".$experiment_info["id"], $experiment_info["name"], "experiment");
					$observatoryNode->addChild($experimentNode);
				}
				else
				{
					$experimentNode = new TreeNodeObject($missionNode->getId()."_".$experiment_info["id"], $experiment_info["name"], "experiment");
					$missionNode->addChild($experimentNode);
				}
			}
		}
		
		$datasetNode = NULL;
		if (count($instruments_info) == 0)
		{
			//Add dataset
			if ($experiment_info != NULL)
			{
				$datasetNode = new TreeNodeObject($experimentNode->getId()."_".$dataset["id"], $dataset["name"], "dataset");
				$experimentNode->addChild($datasetNode);
			}
			else if($observatory_info != NULL)
			{
				$datasetNode = new TreeNodeObject($observatoryNode->getId()."_".$dataset["id"], $dataset["name"], "dataset");
				$observatoryNode->addChild($datasetNode);
			}
			else
			{
				$datasetNode = new TreeNodeObject($missionNode->getId()."_".$dataset["id"], $dataset["name"], "dataset");
				$missionNode->addChild($datasetNode);
			}
		}
		else
		{
			foreach ($instruments_info as $instrument_info)
			{
				$instrumentNode = NULL;
				if ($experiment_info != NULL)
					$instrumentNode = $experimentNode->getChildById($experimentNode->getId()."_".$instrument_info["id"]);
				else if ($observatory_info != NULL)
					$instrumentNode = $observatoryNode->getChildById($observatoryNode->getId()."_".$instrument_info["id"]);
				else
					$instrumentNode = $missionNode->getChildById($missionNode->getId()."_".$instrument_info["id"]);
					
				if (!isset($instrumentNode))
				{
					//Add instruments
					if ($experiment_info != NULL)
					{
						$instrumentNode = new TreeNodeObject($experimentNode->getId()."_".$instrument_info["id"], $instrument_info["name"], "instrument");
						$experimentNode->addChild($instrumentNode);
					}
					else if ($observatory_info != NULL)
					{
						$instrumentNode = new TreeNodeObject($observatoryNode->getId()."_".$instrument_info["id"], $instrument_info["name"], "instrument");
						$observatoryNode->addChild($instrumentNode);
					}
					else
					{
						$instrumentNode = new TreeNodeObject($missionNode->getId()."_".$instrument_info["id"], $instrument_info["name"], "instrument");
						$missionNode->addChild($instrumentNode);
					}
				}
			
				//Add dataset
				$datasetNode = new TreeNodeObject($instrumentNode->getId()."_".$dataset["id"], $dataset["name"], "dataset");
				$instrumentNode->addChild($datasetNode);
			}
		}		
	}
	
	return $rootNode->toArray();
}

}

?>