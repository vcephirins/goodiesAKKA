<?php

class TreeNodeObject
{
private $id   = "";
private $text = "";
private $type = "";
private $children = array();

function __construct($id, $text, $type)
{
	$this->id = $id;
	$this->text = $text;
	$this->type = $type;
}

public function getId()
{
	return $this->id;
}

public function getText()
{
	return $this->text;
}

public function addChild($childNode)
{
	//sort by node text
	$nodeAdded = false;
	for ($i = 0; $i < count($this->children); ++$i)
	{
		if (strcmp (strtolower($this->children[$i]->getText()), strtolower($childNode->getText())) >= 0)
		{
			array_splice($this->children, $i, 0, array($childNode));
			$nodeAdded = true;
			break;
		}
	}

	if (!$nodeAdded)
	{
		//Add to end
		$this->children[] = $childNode;
		return;
	}
}

public function getChildById($child_id)
{
	foreach ($this->children as $child)
	{
		if ($child->getId() == $child_id)
			return $child;
	}
	return NULL;
}

public function toArray()
{
	$node_array = array(
		"id" => $this->id,
		"text" => $this->text,
		"type" => $this->type,
		"children" => array()
	);
	
	foreach ($this->children as $child)
		$node_array["children"][] = $child->toArray();
		
	return $node_array;
}

}

?>
