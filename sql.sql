CREATE TABLE `ip_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(32) DEFAULT NULL,
  `address` varchar(64) DEFAULT NULL,
  `keyword` varchar(64) DEFAULT '',
  `url` varchar(256) DEFAULT '',
  `error` varchar(64) DEFAULT '',
  `page` int(11) DEFAULT '-1' COMMENT '目标所在页',
  `rank` int(11) DEFAULT '-1' COMMENT '排名',
  `created_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;