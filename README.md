# wfhtoday-st
Tool that lets you see who else is wfh today, and for what reason

```
CREATE TABLE `wfhtoday` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(40) DEFAULT NULL,
  `deviceid` varchar(40) DEFAULT NULL,
  `residence` varchar(100) DEFAULT NULL,
  `office` varchar(100) DEFAULT NULL,
  `timestamp` bigint(11) DEFAULT NULL,
  `commuteMode` tinyint(2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```
