-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 23, 2023 at 01:35 AM
-- Server version: 8.0.31
-- PHP Version: 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `events`
--
CREATE DATABASE IF NOT EXISTS `events` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `events`;
-- --------------------------------------------------------

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
CREATE TABLE IF NOT EXISTS `events` (
  `eventid` int NOT NULL AUTO_INCREMENT,
  `eventtitle` varchar(1000) NOT NULL,
  `eventdescription` varchar(1000) NOT NULL,
  `eventdate` varchar(20) NOT NULL,
  `starttime` varchar(20) NOT NULL,
  `endtime` varchar(20) NOT NULL,
  `maxpax` int DEFAULT NULL,
  `currentpax` int DEFAULT NULL,
  PRIMARY KEY (`eventid`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `events`
--

INSERT INTO `events` (`eventid`, `eventtitle`, `eventdescription`, `eventdate`, `starttime`, `endtime`, `maxpax`, `currentpax`) VALUES
(1, 'Beach Clean Up (ECP)', 
  'Volunteer program to conduct regular beach cleaning activities to promote environmental conservation and sustainability.
  Participants engage in collecting trash, sorting them for recycling, and properly disposing of waste materials.', 
  '20/03/2023', '8am', '2pm', 50, 0),
(2, 'Project Community Garden', 
  'Promote sustainable food production by creating community gardens where participants can grow their own organic produce, 
  while also learning about composting and other sustainable gardening practices.', 
  '26/04/2023', '10am', '2pm', 30, 0),
(3, 'Recycling Competition', 
  'Encourage participants to reduce waste and promote recycling by challenging them to come up with creative ways to recycle 
  common household items, such as plastic bottles, cans, and cardboard boxes. Participants are expected to collect and repurpose
   these items in unique and innovative ways, while also learning about the environmental benefits of recycling.', 
  '04/05/2023', '1pm', '3pm', 40, 0);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
