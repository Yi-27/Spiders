-- 东方财富数据库
CREATE DATABASE IF NOT EXISTS `dfcf` CHARACTER SET UTF8;

-- 使用数据库
USE `dfcf`;

-- 创建stockList表
CREATE TABLE IF NOT EXISTS `stockList`(
  `id` varchar(8) NOT NULL PRIMARY KEY,
  `name` varchar(32) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
-- EBGINE为存储引擎