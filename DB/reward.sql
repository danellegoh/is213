-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jun 12, 2020 at 02:17 AM
-- Server version: 5.7.19
-- PHP Version: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `reward`
CREATE DATABASE IF NOT EXISTS `rewards` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `rewards`;
--
-- Table structure for table `rewards`
--

DROP TABLE IF EXISTS `rewards`;
CREATE TABLE IF NOT EXISTS `rewards` (
  `rewardID` char(100) NOT NULL,
  `rewardName` varchar(100) NOT NULL,
  `quantity` int NOT NULL,
  `discount` float NOT NULL,
  `tier` varchar(10) NOT NULL,
  `month` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `special` boolean NOT NULL,
  PRIMARY KEY (`rewardID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `rewards`
--

INSERT INTO `rewards` (`rewardID`, `rewardName`, `quantity`, `discount`, `tier`, `month`, `special`) VALUES
('1', '5% discount at 7-Eleven', 0, 0.05, 'Bronze', '3', 0),
('2', '7% discount at Fairprice', 125, 0.07, 'Silver', '3', 0),
('3', '10% discount at Sheng Siong', 100, 0.1, 'Gold', '3', 0),
('4', '2% discount at Sheng Siong', 150, 0.02, 'Bronze', '4', 0),
('5', '5% discount at 7-Eleven', 125, 0.05, 'Silver', '4', 0),
('6', '7% discount at Cold Storage', 100, 0.07, 'Gold', '4', 0),
('7', '[Earth Day] 8% discount at Fairprice', 100, 0.08, 'Bronze', '4', 1),
('8', '[Earth Day] 8% discount at Fairprice', 100, 0.08, 'Silver', '4', 1),
('9', '[Earth Day] 8% discount at Fairprice', 100, 0.08, 'Gold', '4', 1);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;