<?php

abstract class CdppSipadXmlResultParserAbstract
{
protected $doc   = NULL;
protected $xpath = NULL;

function __construct()
{
}

abstract public function parse();

public function loadFromString($xml_string)
{
	$this->doc = new DOMDocument();
	$this->xpath = NULL;

	if ($this->doc->loadXML($xml_string) === FALSE)
	{
		$this->doc = NULL;
		return false;
	}
		
	$this->xpath = new DOMXpath($this->doc);
	
	return true;
}

public function isLoaded()
{
	return (($this->doc != NULL) && ($this->xpath != NULL));
}

protected function getStringAttributeValue($attribute_node)
{
	$attribute_node_path = $attribute_node->getNodePath();
	
	$value_nodes = $this->xpath->query($attribute_node_path."/values/value");
	
	if ($value_nodes->length != 1)
		return "";
		
	return $value_nodes->item(0)->nodeValue;
}

protected function getStringListAttributeValue($attribute_node)
{
	$attribute_node_path = $attribute_node->getNodePath();
	
	$value_nodes = $this->xpath->query($attribute_node_path."/values/value");
	
	$value_list = array();
	foreach ($value_nodes as $value_node)
	{
		if (!in_array($value_node->nodeValue, $value_list))
			$value_list[] = $value_node->nodeValue;
	}
		
	return $value_list;
}
}

?>
