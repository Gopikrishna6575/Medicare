-- MySQL dump 10.13  Distrib 8.0.35, for Win64 (x86_64)
--
-- Host: localhost    Database: db
-- ------------------------------------------------------
-- Server version	8.0.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `admin_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(25) NOT NULL,
  `email` varchar(55) NOT NULL,
  `password` varchar(200) NOT NULL,
  PRIMARY KEY (`admin_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'saketh','kgk6575@gmail.com','$2b$12$j0gufBQVhifikLstz.UJ8Of6MiWMU68gT40MiC8NUtLS7mm.vw16K'),(2,'Gopikrishna','raju467678@gmail.com','$2b$12$hmiAYB8OD.ydDkRP52SAM.opGXdsgbMDuxkmVhqi/E2KoGDPckKxm'),(3,'ram tharak','nchowdary059@gmail.com','$2b$12$TqBaFoY3WA/fPftqRaAr.uXmc46IkU.SwptSscwlCZix04/QlacRG');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appointments`
--

DROP TABLE IF EXISTS `appointments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointments` (
  `appointment_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `email` varchar(255) NOT NULL,
  `appointment_date` date NOT NULL,
  `appointment_time` time NOT NULL,
  `suffering_with` varchar(255) NOT NULL,
  `doctor_id` int NOT NULL,
  PRIMARY KEY (`appointment_id`),
  KEY `doctor_id` (`doctor_id`),
  CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`doctor_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointments`
--

LOCK TABLES `appointments` WRITE;
/*!40000 ALTER TABLE `appointments` DISABLE KEYS */;
INSERT INTO `appointments` VALUES (1,'sdsd','9638527413','pittalaprasanna33@gmail.com','2024-04-03','01:30:00','Health Check up',20200001),(2,'harsha','9638527413','nchowdary059@gmail.com','2024-04-03','20:26:00','Health Check up',20200001),(3,'python flask','9638527413','kgk6575@gmail.com','2024-04-03','01:38:00','corona',20200001),(4,'Konjeti GopiKrishna','8106429771','raju467678@gmail.com','2024-04-03','03:00:00','Health Check up',20200002),(5,'Konjeti GopiKrishna','9638527413','nchowdary059@gmail.com','2024-04-04','14:39:00','Health Check up',20200002),(6,'Konjeti GopiKrishna','9638527413','nchowdary059@gmail.com','2024-04-04','20:47:00','Health Check up',20200002);
/*!40000 ALTER TABLE `appointments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctors`
--

DROP TABLE IF EXISTS `doctors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctors` (
  `doctor_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(100) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `specialization` varchar(255) NOT NULL,
  `from_time` time DEFAULT '10:00:00',
  `to_time` time DEFAULT '21:00:00',
  PRIMARY KEY (`doctor_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=20200004 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors`
--

LOCK TABLES `doctors` WRITE;
/*!40000 ALTER TABLE `doctors` DISABLE KEYS */;
INSERT INTO `doctors` VALUES (20200001,'Konjeti GopiKrishna','kgk6575@gmail.com','$2b$12$VeIPFB1M/X6DClqR0LRNnOnXuoerDDA7ByynoJidFsgKIA40uEmdq','9638527413','General Surgeon','10:00:00','21:00:00'),(20200002,'python flask','narikellasaiteja8055@gmail.com','$2b$12$b6mjRfgnK6JN/uUv48QdN.wuju03O4qqsTsmKF7gGGGq0.HmMGyfS','9638527413','General Surgeon','10:00:00','21:00:00'),(20200003,'Konjeti GopiKrishna','konjetigopikrishna55@gmail.com','$2b$12$g90LCsrMzd5CiQbwV05ga.D8YfYH6.cFeGrHcwQDurj6xxMssJU.m','9638527413','surgeon','13:19:00','13:20:00');
/*!40000 ALTER TABLE `doctors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctors_request`
--

DROP TABLE IF EXISTS `doctors_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctors_request` (
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `specialization` varchar(255) NOT NULL,
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors_request`
--

LOCK TABLES `doctors_request` WRITE;
/*!40000 ALTER TABLE `doctors_request` DISABLE KEYS */;
INSERT INTO `doctors_request` VALUES ('python','raju467678@gmail.com','9638527413','surgeon');
/*!40000 ALTER TABLE `doctors_request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patientmedicineusage`
--

DROP TABLE IF EXISTS `patientmedicineusage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patientmedicineusage` (
  `patient_id` int NOT NULL,
  `admit_date` date DEFAULT NULL,
  `discharged_on` date DEFAULT NULL,
  `notes` text,
  `injection_name` varchar(255) DEFAULT NULL,
  `injection_cost` decimal(10,2) DEFAULT '0.00',
  `injection_dosage` int DEFAULT '0',
  `tablet_name` varchar(255) DEFAULT NULL,
  `tablet_cost` decimal(10,2) DEFAULT '0.00',
  `tablet_dosage` int DEFAULT '0',
  `room_used` int DEFAULT '0',
  `icu_used` int DEFAULT '0',
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `patientmedicineusage_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patientmedicineusage`
--

LOCK TABLES `patientmedicineusage` WRITE;
/*!40000 ALTER TABLE `patientmedicineusage` DISABLE KEYS */;
INSERT INTO `patientmedicineusage` VALUES (20240001,'2024-01-01','2024-04-02','he was discharged today','dolo',45.00,100,'paracetmol',3.00,250,45,62),(20240001,'2024-01-01','2024-04-02','hii','okkkk',100.00,20,'drug',12.00,100,5,9),(20240001,'2024-04-03','2024-04-03','rfghjkl','junk',1000.00,3,'ram',12.00,45,12,34),(20240001,'2024-03-31','2024-04-03','dicharged','doloed',44.00,2,'rings',548.00,6,2,1);
/*!40000 ALTER TABLE `patientmedicineusage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients`
--

DROP TABLE IF EXISTS `patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients` (
  `patient_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `dob` date NOT NULL,
  `gender` enum('Male','Female','Other') NOT NULL,
  `patient_disease` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `admit_date` date DEFAULT NULL,
  PRIMARY KEY (`patient_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=20240002 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients`
--

LOCK TABLES `patients` WRITE;
/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` VALUES (20240001,'Saketh','kgk6575@gmail.com','$2b$12$5AUPXzKFvWi3hyTsd7zcmO2weiZGQ3.BZ.4WwulIrRnF4nPd7LkbC','9638527413','2024-04-03','Male','eamledu','guntur\r\n','2024-04-27');
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-04 15:11:27
