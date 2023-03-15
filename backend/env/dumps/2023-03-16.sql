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
  PRIMARY KEY (`id`),
  CONSTRAINT `features_cnn_cascade` FOREIGN KEY (`id`) REFERENCES `model` (`features_cnn_id`) ON DELETE CASCADE
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
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `model`
--

LOCK TABLES `model` WRITE;
/*!40000 ALTER TABLE `model` DISABLE KEYS */;
INSERT INTO `model` VALUES
(46,175,'Adamax_categorical_hinge',1,7,5,1,1,10),
(47,177,'Nadam_sparse_categorical_crossentropy',1,8,6,1,1,10),
(48,181,'Nadam_sparse_categorical_crossentropy',1,8,6,1,1,10),
(49,183,'Adadelta_kl_divergence',1,9,7,1,1,10),
(50,187,'Nadam_kl_divergence',1,8,7,1,1,10),
(51,188,'RMSprop_poisson',1,10,8,1,1,10),
(52,189,'RMSprop_poisson',1,10,8,1,1,10),
(53,191,'Adam_poisson',1,11,8,1,1,10),
(54,193,'Adam_poisson',1,11,8,1,1,10),
(55,194,'Nadam_poisson',1,8,8,1,1,10),
(56,196,'Adam_poisson',1,11,8,1,1,10),
(57,198,'Adam_poisson',1,11,8,1,1,10),
(58,200,'Adam_poisson',1,11,8,1,1,10),
(59,206,'Adam_poisson_2023-03-15_12:04:54',1,11,9,1,1,10),
(60,219,'Adam_sparse_categorical_crossentropy',1,11,6,1,1,10),
(61,222,'Adam_sparse_categorical_crossentropy',1,11,6,1,1,10),
(62,224,'Adam_sparse_categorical_crossentropy',1,11,6,1,1,10),
(63,226,'Adam_CCE',1,11,10,1,1,10),
(64,228,'RMSprop_CCE',1,10,10,1,1,10),
(65,235,'Adam_CCE',1,11,10,1,1,10),
(66,237,'Adam_sparse_categorical_crossentropy',1,11,6,1,1,10),
(67,239,'Adam_categorical_hinge',1,11,5,1,1,10),
(68,240,'Adam_kl_divergence',1,11,7,1,1,10),
(69,241,'Adam_kl_divergence',1,11,7,1,1,10),
(70,242,'Nadam_kl_divergence',1,8,7,1,1,10);
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
(46,1,0.233143),
(46,2,0.390818),
(46,3,0.233143),
(46,4,0.190019),
(47,1,0.546286),
(47,2,0.546076),
(47,3,0.546286),
(47,4,0.516189),
(48,1,0.544),
(48,2,0.533737),
(48,3,0.544),
(48,4,0.530898),
(49,1,0.501714),
(49,2,0.282547),
(49,3,0.501714),
(49,4,0.347614),
(50,1,0.508571),
(50,2,0.258645),
(50,3,0.508571),
(50,4,0.3429),
(51,1,0.165714),
(51,2,0.0274612),
(51,3,0.165714),
(51,4,0.0471148),
(52,1,0.508571),
(52,2,0.258645),
(52,3,0.508571),
(52,4,0.3429),
(53,1,0.165714),
(53,2,0.0274612),
(53,3,0.165714),
(53,4,0.0471148),
(54,1,0.325714),
(54,2,0.10609),
(54,3,0.325714),
(54,4,0.160049),
(55,1,0.165714),
(55,2,0.0274612),
(55,3,0.165714),
(55,4,0.0471148),
(56,1,0.165714),
(56,2,0.0274612),
(56,3,0.165714),
(56,4,0.0471148),
(57,1,0.508571),
(57,2,0.258645),
(57,3,0.508571),
(57,4,0.3429),
(58,1,0.325714),
(58,2,0.10609),
(58,3,0.325714),
(58,4,0.160049),
(59,1,0.325714),
(59,2,0.10609),
(59,3,0.325714),
(59,4,0.160049),
(60,1,0.508571),
(60,2,0.258645),
(60,3,0.508571),
(60,4,0.3429),
(61,1,0.548571),
(61,2,0.558358),
(61,3,0.548571),
(61,4,0.528563),
(62,1,0.537143),
(62,2,0.54101),
(62,3,0.537143),
(62,4,0.493563),
(63,1,0.540571),
(63,2,0.540148),
(63,3,0.540571),
(63,4,0.515641),
(64,1,0.541714),
(64,2,0.557018),
(64,3,0.541714),
(64,4,0.50041),
(65,1,0.558857),
(65,2,0.572196),
(65,3,0.558857),
(65,4,0.523232),
(66,1,0.548571),
(66,2,0.556062),
(66,3,0.548571),
(66,4,0.521776),
(67,1,0.193143),
(67,2,0.29796),
(67,3,0.193143),
(67,4,0.123484),
(68,1,0.331429),
(68,2,0.36823),
(68,3,0.331429),
(68,4,0.192287),
(69,1,0.508571),
(69,2,0.258645),
(69,3,0.508571),
(69,4,0.3429),
(70,1,0.508571),
(70,2,0.258645),
(70,3,0.508571),
(70,4,0.3429);
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
) ENGINE=InnoDB AUTO_INCREMENT=243 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_session`
--

LOCK TABLES `user_session` WRITE;
/*!40000 ALTER TABLE `user_session` DISABLE KEYS */;
INSERT INTO `user_session` VALUES
(129,'','',0,'',''),
(130,'','',0,'',''),
(131,'/app/dataset/131/','/app/markup/131_markup.json',0,'/app/models/131/',''),
(132,'/app/dataset/132/','/app/markup/132_markup.json',0,'/app/models/132/',''),
(133,'/app/dataset/133/','/app/markup/133_markup.json',0,'/app/models/133/',''),
(134,'/app/dataset/134/','/app/markup/134_markup.json',0,'',''),
(135,'/app/dataset/135/','/app/markup/135_markup.json',0,'',''),
(136,'test redirect','test redirect',0,'',''),
(137,'/app/dataset/137/','/app/markup/137_markup.json',0,'',''),
(138,'/app/dataset/138/','/app/markup/138_markup.json',0,'',''),
(139,'/app/dataset/139/','/app/markup/139_markup.json',0,'',''),
(140,'test redirect','test redirect',0,'',''),
(141,'/app/dataset/141/','/app/markup/141_markup.json',0,'',''),
(142,'/app/dataset/142/','/app/markup/142_markup.json',0,'/app/models/142/',''),
(143,'/app/dataset/143/','/app/markup/143_markup.json',0,'/app/models/143/',''),
(144,'/app/dataset/144/','/app/markup/144_markup.json',0,'/app/models/144/Adam_sparse_categorical_crossentropy.h5',''),
(145,'/app/dataset/145/','/app/markup/145_markup.json',0,'/app/models/145/Adam_sparse_categorical_crossentropy.h5',''),
(146,'/app/dataset/146/','/app/markup/146_markup.json',0,'/app/models/146/Adam_sparse_categorical_crossentropy.h5',''),
(147,'/app/dataset/147/','/app/markup/147_markup.json',0,'/app/models/147/Adam_sparse_categorical_crossentropy.h5',''),
(148,'/app/dataset/148/','/app/markup/148_markup.json',0,'/app/models/148/Adam_sparse_categorical_crossentropy.h5',''),
(149,'/app/dataset/149/','/app/markup/149_markup.json',0,'/app/models/149/Adam_sparse_categorical_crossentropy.h5',''),
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
(161,'/app/dataset/161/','/app/markup/161_markup.json',0,'/app/models/161/Adam_sparse_categorical_crossentropy.h5','/app/models/161//metrics.json'),
(162,'/app/dataset/162/','/app/markup/162_markup.json',0,'/app/models/162/',''),
(163,'/app/dataset/163/','/app/markup/163_markup.json',0,'/app/models/163/Adamax_sparse_categorical_crossentropy.h5','/app/models/163//metrics.json'),
(164,'/app/dataset/164/','/app/markup/164_markup.json',0,'/app/models/164/',''),
(165,'/app/dataset/165/','/app/markup/165_markup.json',0,'/app/models/165/',''),
(166,'/app/dataset/166/','/app/markup/166_markup.json',0,'/app/models/166/',''),
(167,'/app/dataset/167/','/app/markup/167_markup.json',0,'/app/models/167/',''),
(168,'/app/dataset/168/','/app/markup/168_markup.json',0,'/app/models/168/',''),
(169,'/app/dataset/169/','/app/markup/169_markup.json',0,'/app/models/169/',''),
(170,'/app/dataset/170/','/app/markup/170_markup.json',0,'/app/models/170/',''),
(171,'/app/dataset/171/','/app/markup/171_markup.json',0,'/app/models/171/',''),
(172,'/app/dataset/172/','/app/markup/172_markup.json',0,'/app/models/172/',''),
(173,'/app/dataset/173/','/app/markup/173_markup.json',0,'/app/models/173/Adamax_categorical_hinge.h5',''),
(174,'/app/dataset/174/','/app/markup/174_markup.json',0,'/app/models/174/Adamax_categorical_hinge.h5',''),
(175,'/app/dataset/175/','/app/markup/175_markup.json',0,'/app/models/175/Adamax_categorical_hinge.h5',''),
(176,'/app/dataset/176/','/app/markup/176_markup.json',0,'/app/models/176/',''),
(177,'/app/dataset/177/','/app/markup/177_markup.json',0,'/app/models/177/Nadam_sparse_categorical_crossentropy.h5',''),
(178,'/app/dataset/178/','/app/markup/178_markup.json',0,'/app/models/178/',''),
(179,'/app/dataset/179/','/app/markup/179_markup.json',0,'/app/models/179/',''),
(180,'/app/dataset/180/','/app/markup/180_markup.json',0,'/app/models/180/',''),
(181,'/app/dataset/181/','/app/markup/181_markup.json',0,'/app/models/181/Nadam_sparse_categorical_crossentropy.h5',''),
(182,'/app/dataset/182/','/app/markup/182_markup.json',0,'/app/models/182/',''),
(183,'/app/dataset/183/','/app/markup/183_markup.json',0,'/app/models/183/Adadelta_kl_divergence.h5',''),
(184,'/app/dataset/184/','/app/markup/184_markup.json',0,'/app/models/184/',''),
(185,'/app/dataset/185/','/app/markup/185_markup.json',0,'',''),
(186,'/app/dataset/186/','/app/markup/186_markup.json',0,'',''),
(187,'/app/dataset/187/','/app/markup/187_markup.json',0,'/app/models/187/Nadam_kl_divergence.h5','/app/models/187//metrics.json'),
(188,'/app/dataset/188/','/app/markup/188_markup.json',0,'/app/models/188/RMSprop_poisson.h5','/app/models/188//metrics.json'),
(189,'/app/dataset/189/','/app/markup/189_markup.json',0,'/app/models/189/RMSprop_poisson.h5','/app/models/189//metrics.json'),
(190,'/app/dataset/190/','/app/markup/190_markup.json',0,'/app/models/190/',''),
(191,'/app/dataset/191/','/app/markup/191_markup.json',0,'/app/models/191/Adam_poisson.h5','/app/models/191//metrics.json'),
(192,'/app/dataset/192/','/app/markup/192_markup.json',0,'/app/models/192/',''),
(193,'/app/dataset/193/','/app/markup/193_markup.json',0,'/app/models/193/Adam_poisson.h5','/app/models/193//metrics.json'),
(194,'/app/dataset/194/','/app/markup/194_markup.json',0,'/app/models/194/Nadam_poisson.h5','/app/models/194//metrics.json'),
(195,'/app/dataset/195/','/app/markup/195_markup.json',0,'/app/models/195/',''),
(196,'/app/dataset/196/','/app/markup/196_markup.json',0,'/app/models/196/Adam_poisson.h5','/app/models/196//metrics.json'),
(197,'/app/dataset/197/','/app/markup/197_markup.json',0,'/app/models/197/',''),
(198,'/app/dataset/198/','/app/markup/198_markup.json',0,'/app/models/198/Adam_poisson.h5','/app/models/198//metrics.json'),
(199,'/app/dataset/199/','/app/markup/199_markup.json',0,'/app/models/199/',''),
(200,'/app/dataset/200/','/app/markup/200_markup.json',0,'/app/models/200/Adam_poisson.h5','/app/models/200//metrics.json'),
(201,'/app/dataset/201/','/app/markup/201_markup.json',0,'/app/models/201/',''),
(202,'/app/dataset/202/','/app/markup/202_markup.json',0,'/app/models/202/',''),
(203,'/app/dataset/203/','/app/markup/203_markup.json',0,'/app/models/203/',''),
(204,'/app/dataset/204/','/app/markup/204_markup.json',0,'/app/models/204/',''),
(205,'/app/dataset/205/','/app/markup/205_markup.json',0,'/app/models/205/',''),
(206,'/app/dataset/206/','/app/markup/206_markup.json',0,'/app/models/206/Adam_poisson_2023-03-15_12:04:54.h5','/app/models/206//metrics.json'),
(207,'/app/dataset/207/','/app/markup/207_markup.json',0,'/app/models/207/',''),
(208,'/app/dataset/208/','/app/markup/208_markup.json',0,'/app/models/208/',''),
(209,'/app/dataset/209/','/app/markup/209_markup.json',0,'/app/models/209/',''),
(210,'/app/dataset/210/','/app/markup/210_markup.json',0,'/app/models/210/',''),
(211,'/app/dataset/211/','/app/markup/211_markup.json',0,'/app/models/211/',''),
(212,'/app/dataset/212/','/app/markup/212_markup.json',0,'/app/models/212/',''),
(213,'/app/dataset/213/','/app/markup/213_markup.json',0,'/app/models/213/',''),
(214,'/app/dataset/214/','/app/markup/214_markup.json',0,'/app/models/214/',''),
(215,'/app/dataset/215/','/app/markup/215_markup.json',0,'/app/models/215/',''),
(216,'/app/dataset/216/','/app/markup/216_markup.json',0,'/app/models/216/',''),
(217,'/app/dataset/217/','/app/markup/217_markup.json',0,'/app/models/217/',''),
(218,'/app/dataset/218/','/app/markup/218_markup.json',0,'/app/models/218/',''),
(219,'/app/dataset/219/','/app/markup/219_markup.json',0,'/app/models/219/Adam_sparse_categorical_crossentropy.h5','/app/models/219//metrics.json'),
(220,'/app/dataset/220/','/app/markup/220_markup.json',0,'/app/models/220/',''),
(221,'/app/dataset/221/','/app/markup/221_markup.json',0,'/app/models/221/',''),
(222,'/app/dataset/222/','/app/markup/222_markup.json',0,'/app/models/222/Adam_sparse_categorical_crossentropy.h5','/app/models/222//metrics.json'),
(223,'/app/dataset/223/','/app/markup/223_markup.json',0,'/app/models/223/',''),
(224,'/app/dataset/224/','/app/markup/224_markup.json',0,'/app/models/224/Adam_sparse_categorical_crossentropy.h5','/app/models/224//metrics.json'),
(225,'/app/dataset/225/','/app/markup/225_markup.json',0,'/app/models/225/',''),
(226,'/app/dataset/226/','/app/markup/226_markup.json',0,'/app/models/226/Adam_CCE.h5','/app/models/226//metrics.json'),
(227,'/app/dataset/227/','/app/markup/227_markup.json',0,'/app/models/227/',''),
(228,'/app/dataset/228/','/app/markup/228_markup.json',0,'/app/models/228/RMSprop_CCE.h5','/app/models/228//metrics.json'),
(229,'/app/dataset/229/','/app/markup/229_markup.json',0,'/app/models/229/',''),
(230,'/app/dataset/230/','/app/markup/230_markup.json',0,'/app/models/230/',''),
(231,'/app/dataset/231/','/app/markup/231_markup.json',0,'/app/models/231/',''),
(232,'/app/dataset/232/','/app/markup/232_markup.json',0,'/app/models/232/',''),
(233,'/app/dataset/233/','/app/markup/233_markup.json',0,'/app/models/233/',''),
(234,'/app/dataset/234/','/app/markup/234_markup.json',0,'/app/models/234/',''),
(235,'/app/dataset/235/','/app/markup/235_markup.json',0,'/app/models/235/Adam_CCE.h5','/app/models/235//metrics.json'),
(236,'/app/dataset/236/','/app/markup/236_markup.json',0,'/app/models/236/',''),
(237,'/app/dataset/237/','/app/markup/237_markup.json',0,'',''),
(238,'/app/dataset/238/','/app/markup/238_markup.json',0,'',''),
(239,'/app/dataset/239/','/app/markup/239_markup.json',0,'/app/models/239/Adam_categorical_hinge.h5','/app/models/239//metrics.json'),
(240,'/app/dataset/240/','/app/markup/240_markup.json',0,'/app/models/240/Adam_kl_divergence.h5','/app/models/240//metrics.json'),
(241,'/app/dataset/241/','/app/markup/241_markup.json',0,'/app/models/241/Adam_kl_divergence.h5','/app/models/241//metrics.json'),
(242,'/app/dataset/242/','/app/markup/242_markup.json',0,'/app/models/242/Nadam_kl_divergence.h5','/app/models/242//metrics.json');
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
(0,'string','skjfdnv@yandex.ru');
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

-- Dump completed on 2023-03-16  1:03:38
