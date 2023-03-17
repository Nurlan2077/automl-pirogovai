-- MariaDB dump 10.19  Distrib 10.10.3-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: 127.0.0.1    Database: auto_model_learning
-- ------------------------------------------------------
-- Server version	10.10.3-MariaDB-1:10.10.3+maria~ubu2204

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `auto_model_learning`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `auto_model_learning` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;

USE `auto_model_learning`;

--
-- Table structure for table `features_cnn`
--

DROP TABLE IF EXISTS `features_cnn`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `features_cnn` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(55) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `features_cnn`
--

LOCK TABLES `features_cnn` WRITE;
/*!40000 ALTER TABLE `features_cnn` DISABLE KEYS */;
INSERT INTO `features_cnn` VALUES
(1,'placeholder');
/*!40000 ALTER TABLE `features_cnn` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loss_function`
--

DROP TABLE IF EXISTS `loss_function`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `loss_function` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(55) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loss_function`
--

LOCK TABLES `loss_function` WRITE;
/*!40000 ALTER TABLE `loss_function` DISABLE KEYS */;
INSERT INTO `loss_function` VALUES
(5,'categorical_hinge'),
(6,'sparse_categorical_crossentropy'),
(7,'kl_divergence'),
(8,'poisson'),
(9,'poisson_2023-03-15_12:04:54'),
(10,'CCE');
/*!40000 ALTER TABLE `loss_function` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `metric`
--

DROP TABLE IF EXISTS `metric`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `metric` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(55) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metric`
--

LOCK TABLES `metric` WRITE;
/*!40000 ALTER TABLE `metric` DISABLE KEYS */;
INSERT INTO `metric` VALUES
(1,'accuracy'),
(2,'precision'),
(3,'recall'),
(4,'f1-score');
/*!40000 ALTER TABLE `metric` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `model`
--

DROP TABLE IF EXISTS `model`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `model` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `session_id` int(11) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `features_cnn_id` int(11) DEFAULT NULL,
  `optimizer_id` int(11) DEFAULT NULL,
  `loss_function_id` int(11) DEFAULT NULL,
  `augmentation` int(11) DEFAULT NULL,
  `learning_speed` float DEFAULT NULL,
  `epoch_count` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_session_id` (`session_id`),
  KEY `fk_features_cnn_id` (`features_cnn_id`),
  KEY `fk_optimizer_id` (`optimizer_id`),
  KEY `fk_loss_function_id` (`loss_function_id`),
  CONSTRAINT `fk_features_cnn` FOREIGN KEY (`features_cnn_id`) REFERENCES `features_cnn` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_loss_function` FOREIGN KEY (`loss_function_id`) REFERENCES `loss_function` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_optimizer_id` FOREIGN KEY (`optimizer_id`) REFERENCES `optimizer` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_session_id` FOREIGN KEY (`session_id`) REFERENCES `user_session` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=74 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `model`
--

LOCK TABLES `model` WRITE;
/*!40000 ALTER TABLE `model` DISABLE KEYS */;
INSERT INTO `model` VALUES
(73,247,'Nadam_categorical_hinge',1,8,5,1,1,10);
/*!40000 ALTER TABLE `model` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `model_metric`
--

DROP TABLE IF EXISTS `model_metric`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `model_metric` (
  `model_id` int(11) NOT NULL,
  `metric_id` int(11) NOT NULL,
  `metric_value` float NOT NULL,
  KEY `model_id` (`model_id`),
  KEY `metric_id` (`metric_id`),
  CONSTRAINT `fk_metric_id` FOREIGN KEY (`metric_id`) REFERENCES `metric` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_model_id` FOREIGN KEY (`model_id`) REFERENCES `model` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `model_metric`
--

LOCK TABLES `model_metric` WRITE;
/*!40000 ALTER TABLE `model_metric` DISABLE KEYS */;
INSERT INTO `model_metric` VALUES
(73,1,0.325714),
(73,2,0.106211),
(73,3,0.325714),
(73,4,0.160187);
/*!40000 ALTER TABLE `model_metric` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `optimizer`
--

DROP TABLE IF EXISTS `optimizer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `optimizer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(55) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `optimizer`
--

LOCK TABLES `optimizer` WRITE;
/*!40000 ALTER TABLE `optimizer` DISABLE KEYS */;
INSERT INTO `optimizer` VALUES
(7,'Adamax'),
(8,'Nadam'),
(9,'Adadelta'),
(10,'RMSprop'),
(11,'Adam');
/*!40000 ALTER TABLE `optimizer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_session`
--

DROP TABLE IF EXISTS `user_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_session` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dataset_path` varchar(255) NOT NULL,
  `data_markup_path` varchar(255) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `model_path` varchar(255) DEFAULT NULL,
  `metrics_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_user_id` (`user_id`),
  CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=248 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_session`
--

LOCK TABLES `user_session` WRITE;
/*!40000 ALTER TABLE `user_session` DISABLE KEYS */;
INSERT INTO `user_session` VALUES
(243,'/app/dataset/243/','/app/markup/243_markup.json',0,'/app/models/243/Adam_kl_divergence.h5','/app/models/243//metrics.json'),
(244,'/app/dataset/244/','/app/markup/244_markup.json',0,'/app/models/244/',''),
(245,'','',1837,'',''),
(246,'/app/dataset/246/','/app/markup/246_markup.json',0,'/app/models/246/Nadam_categorical_hinge.h5','/app/models/246//metrics.json'),
(247,'/app/dataset/247/','/app/markup/247_markup.json',0,'/app/models/247/Nadam_categorical_hinge.h5','/app/models/247//metrics.json');
/*!40000 ALTER TABLE `user_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(55) NOT NULL,
  `email` varchar(55) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
(0,'Maria','mmakhaladze@edu.hse.ru'),
(1837,'Test user','testuser@gmail.com');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-03-17  0:41:57
