<?php

class DatabaseManager
{
private static $_instance = null;

private $database_path = "./";
private $current_session_dir = "";

public static function getInstance()
{
	if(is_null(self::$_instance))
	{
		self::$_instance = new DatabaseManager();
	}

	return self::$_instance;
}

public function setPath($path)
{
	$this->database_path = $path;
	if (!is_dir($this->database_path))
		mkdir($this->database_path, 0777);
}

public function createNewSession()
{
	$handle = null;
	//Load sessions file
	$handle = fopen($this->getSessionsFilePath(),"a+");
	
	//Lock sessions file
	if (flock($handle, LOCK_EX))
	{
		//load existing sessions
		$fileSize = filesize($this->getSessionsFilePath());
		$sessions_list = null;
		if ($fileSize > 0)
		{
			//Load content
			$file_data = fread($handle, $fileSize);
			$sessions_list = json_decode($file_data);
		}
		else
			$sessions_list = array();

		//Init new session
		$datetime = new DateTime();
		$this->current_session_dir = "session_".$datetime->getTimestamp();
		if (!$this->initSession())
		{
			flock($handle, LOCK_UN); // release the lock
			fclose($handle);
			return false;
		}
		
		//add new session to sessions file
		$crtISOTime = $datetime->format('c');
		$results_list[] = array(
			"date"        => $crtISOTime,
			"session_dir" => $this->current_session_dir,
			"ready"       => false
		);
		ftruncate ($handle , 0);
		fwrite($handle, json_encode($results_list));
		fflush($handle);
		flock($handle, LOCK_UN); // release the lock
		fclose($handle);
	}
	else
		return false;
	return true;
}

public function getSessionDataPath()
{
	if ($this->current_session_dir == "")
		return FALSE;
	return $this->database_path."/".$this->current_session_dir."/data/";
}

public function getSessionSipadServiceDataPath()
{
	if ($this->current_session_dir == "")
		return FALSE;
	return $this->database_path."/".$this->current_session_dir."/sipad-data/";
}

public function getSessionTreePath()
{
	if ($this->current_session_dir == "")
		return FALSE;
	return $this->database_path."/".$this->current_session_dir."/tree/";
}

private function __construct()
{
}

private function initSession()
{
	if ($this->current_session_dir == NULL)
		return FALSE;
	//Create session dircetory
	mkdir($this->getCurrentSessionPath(),0777);
	//Create data directory
	mkdir($this->getSessionDataPath(),0777);
	//Create tree directory
	mkdir($this->getSessionTreePath(),0777);
	//Create sipad service data directory
	mkdir($this->getSessionSipadServiceDataPath(),0777);
	return true;
}

private function getSessionsFilePath()
{
	return $this->database_path."/sessions.json";
}

private function getCurrentSessionPath()
{
	return $this->database_path."/".$this->current_session_dir."/";
}

};

?>