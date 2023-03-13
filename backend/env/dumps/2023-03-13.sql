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
(1,'test');
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loss_function`
--

LOCK TABLES `loss_function` WRITE;
/*!40000 ALTER TABLE `loss_function` DISABLE KEYS */;
INSERT INTO `loss_function` VALUES
(1,'sparse_categorical_crossentropy'),
(2,'categorical_hinge'),
(3,'kl_divergence'),
(4,'poisson');
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
  CONSTRAINT `fk_features_cnn_id` FOREIGN KEY (`features_cnn_id`) REFERENCES `features_cnn` (`id`),
  CONSTRAINT `fk_loss_function_id` FOREIGN KEY (`loss_function_id`) REFERENCES `loss_function` (`id`),
  CONSTRAINT `fk_optimizer_id` FOREIGN KEY (`optimizer_id`) REFERENCES `optimizer` (`id`),
  CONSTRAINT `fk_session_id` FOREIGN KEY (`session_id`) REFERENCES `user_session` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `model`
--

LOCK TABLES `model` WRITE;
/*!40000 ALTER TABLE `model` DISABLE KEYS */;
INSERT INTO `model` VALUES
(30,135,'Adam_sparse_categorical_crossentropy',1,1,1,1,1,10),
(31,137,'Adam_sparse_categorical_crossentropy',1,1,1,1,1,10),
(32,139,'Adam_sparse_categorical_crossentropy',1,1,1,1,1,10),
(33,141,'Adam_sparse_categorical_crossentropy',1,1,1,1,1,10),
(34,144,'Adam_sparse_categorical_crossentropy',1,1,1,1,1,10),
(35,145,'Adam_sparse_categorical_crossentropy',1,1,1,1,1,10),
(36,146,'Adam_sparse_categorical_crossentropy',1,1,1,1,1,10),
(37,147,'Adam_sparse_categorical_crossentropy',1,1,1,1,1,10),
(38,148,'Adam_sparse_categorical_crossentropy',1,1,1,1,1,10),
(39,149,'Adam_sparse_categorical_crossentropy',1,1,1,1,1,10),
(40,157,'Adam_sparse_categorical_crossentropy',1,1,1,1,1,10),
(41,158,'Adam_sparse_categorical_crossentropy',1,1,1,1,1,10),
(42,159,'Adam_sparse_categorical_crossentropy',1,1,1,1,1,10),
(43,160,'Adam_sparse_categorical_crossentropy',1,1,1,1,1,10),
(44,161,'Adam_sparse_categorical_crossentropy',1,1,1,1,1,10);
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
  CONSTRAINT `metric_id` FOREIGN KEY (`metric_id`) REFERENCES `metric` (`id`),
  CONSTRAINT `model_id` FOREIGN KEY (`model_id`) REFERENCES `model` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `model_metric`
--

LOCK TABLES `model_metric` WRITE;
/*!40000 ALTER TABLE `model_metric` DISABLE KEYS */;
INSERT INTO `model_metric` VALUES
(30,1,0.508571),
(30,2,0.258645),
(30,3,0.508571),
(30,4,0.3429),
(31,1,0.544),
(31,2,0.551006),
(31,3,0.544),
(31,4,0.498064),
(32,1,0.508571),
(32,2,0.258645),
(32,3,0.508571),
(32,4,0.3429),
(33,1,0.508571),
(33,2,0.258645),
(33,3,0.508571),
(33,4,0.3429),
(34,1,0.542857),
(34,2,0.546499),
(34,3,0.542857),
(34,4,0.509597),
(35,1,0.554286),
(35,2,0.569799),
(35,3,0.554286),
(35,4,0.503523),
(36,1,0.545143),
(36,2,0.560706),
(36,3,0.545143),
(36,4,0.473916),
(37,1,0.518857),
(37,2,0.577444),
(37,3,0.518857),
(37,4,0.404059),
(38,1,0.36),
(38,2,0.408),
(38,3,0.36),
(38,4,0.303397),
(39,1,0.437714),
(39,2,0.41653),
(39,3,0.437714),
(39,4,0.394047),
(40,1,0.537143),
(40,2,0.550399),
(40,3,0.537143),
(40,4,0.495141),
(41,1,0.531429),
(41,2,0.559307),
(41,3,0.531429),
(41,4,0.455995),
(42,1,0.550857),
(42,2,0.599591),
(42,3,0.550857),
(42,4,0.498486),
(43,1,0.530286),
(43,2,0.561454),
(43,3,0.530286),
(43,4,0.414269),
(44,1,0.546286),
(44,2,0.552405),
(44,3,0.546286),
(44,4,0.508446);
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `optimizer`
--

LOCK TABLES `optimizer` WRITE;
/*!40000 ALTER TABLE `optimizer` DISABLE KEYS */;
INSERT INTO `optimizer` VALUES
(1,'Adam'),
(2,'Nadam'),
(3,'Adadelta'),
(4,'RMSprop');
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
  `model_path` varchar(55) DEFAULT '',
  `metrics_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_user_id` (`user_id`),
  CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=162 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_session`
--

LOCK TABLES `user_session` WRITE;
/*!40000 ALTER TABLE `user_session` DISABLE KEYS */;
INSERT INTO `user_session` VALUES
(129,'','',0,'',NULL),
(130,'','',0,'',NULL),
(131,'/app/dataset/131/','/app/markup/131_markup.json',0,'/app/models/131/',NULL),
(132,'/app/dataset/132/','/app/markup/132_markup.json',0,'/app/models/132/',NULL),
(133,'/app/dataset/133/','/app/markup/133_markup.json',0,'/app/models/133/',NULL),
(134,'/app/dataset/134/','/app/markup/134_markup.json',0,'',NULL),
(135,'/app/dataset/135/','/app/markup/135_markup.json',0,'',NULL),
(136,'test redirect','test redirect',0,'',NULL),
(137,'/app/dataset/137/','/app/markup/137_markup.json',0,'',NULL),
(138,'/app/dataset/138/','/app/markup/138_markup.json',0,'',NULL),
(139,'/app/dataset/139/','/app/markup/139_markup.json',0,'',NULL),
(140,'test redirect','test redirect',0,'',NULL),
(141,'/app/dataset/141/','/app/markup/141_markup.json',0,'',NULL),
(142,'/app/dataset/142/','/app/markup/142_markup.json',0,'/app/models/142/',NULL),
(143,'/app/dataset/143/','/app/markup/143_markup.json',0,'/app/models/143/',NULL),
(144,'/app/dataset/144/','/app/markup/144_markup.json',0,'/app/models/144/Adam_sparse_categorical_crossentropy.h5',NULL),
(145,'/app/dataset/145/','/app/markup/145_markup.json',0,'/app/models/145/Adam_sparse_categorical_crossentropy.h5',NULL),
(146,'/app/dataset/146/','/app/markup/146_markup.json',0,'/app/models/146/Adam_sparse_categorical_crossentropy.h5',NULL),
(147,'/app/dataset/147/','/app/markup/147_markup.json',0,'/app/models/147/Adam_sparse_categorical_crossentropy.h5',NULL),
(148,'/app/dataset/148/','/app/markup/148_markup.json',0,'/app/models/148/Adam_sparse_categorical_crossentropy.h5',NULL),
(149,'/app/dataset/149/','/app/markup/149_markup.json',0,'/app/models/149/Adam_sparse_categorical_crossentropy.h5',NULL),
(150,'','',0,'',''),
(151,'','',0,'','test'),
(152,'','',0,'','test'),
(153,'','',0,'',''),
(154,'/app/dataset/154/','/app/markup/154_markup.json',0,'/app/models/154/',''),
(155,'/app/dataset/155/','/app/markup/155_markup.json',0,'/app/models/155/',''),
(156,'/app/dataset/156/','/app/markup/156_markup.json',0,'/app/models/156/',''),
(157,'/app/dataset/157/','/app/markup/157_markup.json',0,'/app/models/157/Adam_sparse_categorical_crossentropy.h5','/app/models/157//metrics.json'),
(158,'/app/dataset/158/','/app/markup/158_markup.json',0,'/app/models/158/Adam_sparse_categorical_crossentropy.h5','/app/models/158//metrics.json'),
(159,'/app/dataset/159/','/app/markup/159_markup.json',0,'/app/models/159/Adam_sparse_categorical_crossentropy.h5','/app/models/159//metrics.json'),
(160,'/app/dataset/160/','/app/markup/160_markup.json',0,'/app/models/160/Adam_sparse_categorical_crossentropy.h5','/app/models/160//metrics.json'),
(161,'/app/dataset/161/','/app/markup/161_markup.json',0,'/app/models/161/Adam_sparse_categorical_crossentropy.h5','/app/models/161//metrics.json');
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
(0,'string','skjfdnv@yandex.ru'),
(1,'test','example@gmail.com'),
(2,'Maria','skjfdnv@yandex.ru');
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

-- Dump completed on 2023-03-13 23:42:20
