<?php

abstract class TreeBuilderAbstract
{
protected $datasets = array();
protected $sharedEntities = array();

function __construct($datasets, $sharedEntities)
{
	$this->datasets = $datasets;
	$this->sharedEntities = $sharedEntities;
}

abstract public function build();

protected function getMissionInfoFromId($mission_id)
{
	foreach($this->sharedEntities["missions"] as $mission)
	{
		if ($mission["id"] == $mission_id)
			return $mission;
	}
	return NULL;
}

protected function getObservatoryInfoFromId($observatory_id)
{
	foreach($this->sharedEntities["observatories"] as $observatory)
	{
		if ($observatory["id"] == $observatory_id)
			return $observatory;
	}
	return NULL;
}

protected function getExperimentInfoFromId($experiment_id)
{
	foreach($this->sharedEntities["experiments"] as $experiment)
	{
		if ($experiment["id"] == $experiment_id)
			return $experiment;
	}
	return NULL;
}

protected function getInstrumentInfoFromId($instrument_id)
{
	foreach($this->sharedEntities["instruments"] as $instrument)
	{
		if ($instrument["id"] == $instrument_id)
			return $instrument;
	}
	return NULL;
}

}

?>
